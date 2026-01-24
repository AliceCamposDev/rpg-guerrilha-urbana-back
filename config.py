import os
from pathlib import Path
import obsidiantools.api as otools
import yaml
import logging

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


logger = logging.getLogger(__name__)
logging.basicConfig(level=config["logger_config"]["level"])


def get_logger():
    """Retorna um logger configurado"""
    return logger


VAULT = None


def get_vault_path():
    """Retorna o caminho para o vault Obsidian"""
    paths_to_try = [
        Path(config["vault_path"]),
        Path("public/assets/book"),
        Path("/public/assets/book"),
        Path(__file__).parent / "public" / "assets" / "book",
    ]

    for path in paths_to_try:
        if path.exists():
            logger.info(f"Vault encontrado em: {path.absolute()}")
            return path

    raise FileNotFoundError(f"Nenhum vault encontrado. Diretório atual: {Path.cwd()}")


def init_vault():
    """Inicializa o vault Obsidian"""
    global VAULT

    if VAULT is not None:
        return VAULT

    try:
        vault_path = get_vault_path()
        VAULT = otools.Vault(vault_path).connect().gather()
        logger.info(f"Vault inicializado: {len(VAULT.get_note_metadata())} notas")
        return VAULT
    except Exception as e:
        logger.error(f"Erro ao inicializar vault: {e}")
        raise
