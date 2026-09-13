"""
RAG Agent CLI - Main entry point
"""

import click
import logging
from pathlib import Path

# setup logging once
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)

@click.group()
def cli():
    """RAG Agent - Personal Assistant"""
    logger.info("RAG Agent started")

@cli.command()
@click.option(
    '--path', '-p',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    help='Path to file or directory (default: ./data)'
)

@click.option(
    '--chunk-size',
    type=int,
    default=1000,
    help='chunk size for splitting'
)

@click.option
