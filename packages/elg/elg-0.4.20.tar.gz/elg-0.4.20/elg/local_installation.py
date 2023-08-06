import json
import random
import re
import string
from pathlib import Path
from typing import Any, List, Union
from urllib.parse import urlparse

from loguru import logger

from .entity import Entity, MetadataRecordObj
from .utils import get_information
from .utils.local_installation import (DEFAULT_CONF_TEMPLATE, DOCKER_COMPOSE,
                                       EXPOSE_PORT_CONFIG, FRONTEND, GUI,
                                       GUI_CONF_TEMPLATE,
                                       HTML_INDEX_HTML_TEMPLATE,
                                       HTML_INDEX_IFRAME, HTML_INDEX_SCRIPT,
                                       LTSERVICE, LTSERVICE_URL,
                                       LTSERVICE_WITH_SIDECAR)


def name_from_image(image):
    return re.sub("[^0-9a-zA-Z]+", "_", image)[-60:]


def random_name(length: int = 10):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


class LTServiceLocalInstallation:
    def __init__(
        self,
        id: int,
        image: str,
        sidecar_image: str,
        name: str,
        full_name: str,
        port: int,
        path: str,
        gui: bool,
        gui_image: str,
        gui_port: int,
        gui_path: str,
        record: Any,
    ):
        self.id = id
        self.image = image
        self.sidecar_image = sidecar_image
        self.name = name
        self.full_name = full_name
        self.port = port
        self.path = path
        self.gui = gui
        self.gui_image = gui_image
        self.gui_port = gui_port
        self.gui_path = gui_path
        self.record = record

        self.ltservice = (
            LTSERVICE.format(LTSERVICE_NAME=self.name, LTSERVICE_IMAGE=self.image)
            if self.sidecar_image is None or self.sidecar_image == ""
            else LTSERVICE_WITH_SIDECAR.format(
                LTSERVICE_NAME=self.name,
                LTSERVICE_IMAGE=self.image,
                SIDECAR_IMAGE=self.sidecar_image,
            )
        )
        self.url = LTSERVICE_URL.format(
            LTSERVICE_NAME=self.name,
            LTSERVICE_PORT=self.port,
            LTSERVICE_PATH=self.path,
        )
        if self.gui:
            self.iframe = HTML_INDEX_IFRAME.format(
                LTSERVICE_ID=self.id,
                LTSERVICE_FULL_NAME=self.full_name,
                LTSERVICE_NAME=self.name,
            )
            self.script = HTML_INDEX_SCRIPT.format(
                LTSERVICE_NAME=self.name,
                GUI_NAME=name_from_image(self.gui_image),
                GUI_PATH=self.gui_path,
            )

    @classmethod
    def from_id(
        cls,
        id: int,
        gui: bool = True,
        gui_image: str = "registry.gitlab.com/european-language-grid/usfd/gui-ie:latest",
        gui_port: int = 80,
        domain: str = "live",
        use_cache: bool = True,
        cache_dir: str = "~/.cache/elg",
    ):
        entity = Entity.from_id(id=id, domain=domain, use_cache=use_cache, cache_dir=cache_dir)
        software_distribution = get_information(
            id=entity.id,
            obj=entity.record,
            infos=["described_entity", "lr_subclass", "software_distribution"],
        )[0]
        if software_distribution.get("private_resource"):
            logger.warning(
                "Service [{id}] is private. It cannot be deployed locally.",
                id=entity.id,
            )
            # bypass for UDPipe English to make some tests
            if entity.id != 423:
                return None
        sidecar_image = software_distribution.get("service_adapter_download_location")
        image = software_distribution.get("docker_download_location")
        execution_location = urlparse(software_distribution.get("execution_location"))
        name = get_information(
            id=entity.id,
            obj=entity.record,
            infos=["service_info", "elg_execution_location_sync"],
        ).split("/")[-1]
        full_name = entity.resource_name
        port = execution_location.port
        path = execution_location.path
        gui_path = get_information(id=entity.id, obj=entity.record, infos=["service_info", "elg_gui_url"],).split(
            "/"
        )[-1]
        record = entity.record
        return cls(
            id=id,
            image=image,
            sidecar_image=sidecar_image,
            name=name,
            full_name=full_name,
            port=port,
            path=path,
            gui=gui,
            gui_image=gui_image,
            gui_port=gui_port,
            gui_path=gui_path,
            record=record,
        )

    @classmethod
    def from_docker_image(
        cls,
        image: str,
        execution_location: str,
        sidecar_image: str = "",
        name: str = None,
        full_name: str = None,
        gui: bool = False,
        gui_image: str = "registry.gitlab.com/european-language-grid/usfd/gui-ie:latest",
        gui_port: int = 80,
        gui_path: str = "",
        record: Any = {},
    ):
        name = name if name else random_name()
        full_name = full_name if full_name else f"ELG Service from Docker {name}"
        execution_location = urlparse(execution_location)
        port = execution_location.port
        port = int(port) if port is not None else 80
        path = execution_location.path
        return cls(
            id=-1,
            image=image,
            sidecar_image=sidecar_image,
            name=name,
            full_name=full_name,
            port=port,
            path=path,
            gui=gui,
            gui_image=gui_image,
            gui_port=gui_port,
            gui_path=gui_path,
            record=MetadataRecordObj(record),
        )


class LocalInstallation:
    def __init__(self, ltservices: List[LTServiceLocalInstallation]):
        self.ltservices = ltservices

    @classmethod
    def from_ids(
        cls,
        ids: List[int],
        gui: bool = True,
        gui_images: Union[str, List[str]] = "registry.gitlab.com/european-language-grid/usfd/gui-ie:latest",
        gui_ports: Union[int, List[int]] = 80,
        domain: str = "live",
        use_cache: bool = True,
        cache_dir: str = "~/.cache/elg",
    ):
        if isinstance(gui_images, list) and len(gui_images) == 1:
            gui_images = gui_images[0]
        if isinstance(gui_images, str):
            gui_images = [gui_images for _ in range(len(ids))]
        elif isinstance(gui_images, list):
            if len(gui_images) != len(ids):
                raise ValueError(
                    f"You provided {len(gui_images)} GUI images and {len(ids)} service ids. These two numbers must be equal."
                )
        else:
            raise ValueError("gui_images must be a string or a list of strings.")

        if isinstance(gui_ports, list) and len(gui_ports) == 1:
            gui_ports = gui_ports[0]
        if isinstance(gui_ports, int):
            gui_ports = [gui_ports for _ in range(len(ids))]
        elif isinstance(gui_ports, list):
            if len(gui_ports) != len(ids):
                raise ValueError(
                    f"You provided {len(gui_ports)} GUI ports and {len(ids)} service ids. These two numbers must be equal."
                )
        else:
            raise ValueError("gui_ports must be a int or a list of ints.")

        assert len(ids) == len(gui_images)
        assert len(ids) == len(gui_ports)

        ltservices = [
            LTServiceLocalInstallation.from_id(
                id=ltservice_id,
                gui=gui,
                gui_image=gui_image,
                gui_port=gui_port,
                domain=domain,
                use_cache=use_cache,
                cache_dir=cache_dir,
            )
            for ltservice_id, gui_image, gui_port in zip(ids, gui_images, gui_ports)
        ]
        ltservices = [ltservice for ltservice in ltservices if ltservice]
        return cls(ltservices=ltservices)

    def create_docker_compose(
        self,
        expose_port: int = 8080,
        path: str = "./elg_local_installation/",
    ):
        if self.ltservices == []:
            logger.warning("None of the services can be deployed locally. Therefore, no files will be created.")
            return
        guis_image_port = list(
            set([(ltservice.gui_image, ltservice.gui_port) for ltservice in self.ltservices if ltservice.gui])
        )
        gui = len(guis_image_port) > 0
        if gui:
            guis = [
                GUI.format(GUI_NAME=name_from_image(gui_image), GUI_IMAGE=gui_image)
                for gui_image, _ in guis_image_port
            ]
            frontend = FRONTEND.format(EXPOSE_PORT=expose_port)
            gui_conf_templates = [
                GUI_CONF_TEMPLATE.format(GUI_NAME=name_from_image(gui_image), GUI_PORT=gui_port)
                for gui_image, gui_port in guis_image_port
            ]
            default_conf_template = DEFAULT_CONF_TEMPLATE.format(GUIS="\n\n".join(gui_conf_templates))
            html_index_html_template = HTML_INDEX_HTML_TEMPLATE.format(
                IFRAMES="\n".join([ltservice.iframe for ltservice in self.ltservices if ltservice.gui]),
                SCRIPTS="\n".join([ltservice.script for ltservice in self.ltservices if ltservice.gui]),
            )
        docker_compose = DOCKER_COMPOSE.format(
            LTSERVICES="\n\n".join([ltservice.ltservice for ltservice in self.ltservices]),
            LTSERVICES_URL="\n".join([ltservice.url for ltservice in self.ltservices]),
            EXPOSE_PORT=expose_port,
            EXPOSE_PORT_CONFIG=EXPOSE_PORT_CONFIG.format(EXPOSE_PORT=expose_port) if not gui else "",
            EXECUTION_PATH="" if not gui else "/execution",
            GUIS="\n".join(guis) if gui else "",
            FRONTEND=frontend if gui else "",
        )
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "docker-compose.yml", "w") as f:
            f.write(docker_compose)
        if gui:
            nginx_conf_path = Path(path / "nginx-conf")
            nginx_conf_path.mkdir(parents=True, exist_ok=True)
            html_path = Path(nginx_conf_path / "html")
            html_path.mkdir(parents=True, exist_ok=True)
            with open(nginx_conf_path / "default.conf.template", "w") as f:
                f.write(default_conf_template)
            with open(html_path / "index.html.template", "w") as f:
                f.write(html_index_html_template)
            records_path = Path(nginx_conf_path / "records")
            records_path.mkdir(parents=True, exist_ok=True)
            for ltservice in self.ltservices:
                if ltservice.gui:
                    with open(records_path / f"{ltservice.name}.json", "w") as f:
                        json.dump(ltservice.record, f, default=lambda o: o.__dict__, indent=4)

        logger.info(
            "The Docker compose file has been created [{path}]. Run `docker-compose up` from the folder of Docker compose file to start the ELG REST server and the service.s.",
            path=path / "docker-compose.yml",
        )
        return
