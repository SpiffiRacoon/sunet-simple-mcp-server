import click
from mcp_server import mcp, init_server

@click.command()
@click.option(
    '--entity', '-e', 
    multiple=True, 
    default=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"],
    help="Target Presidio standard tags to actively redact. (e.g. -e PERSON -e IP_ADDRESS)"
)
@click.option(
    '--token', '-t', 
    type=(str, str), 
    multiple=True,
    help="Custom text template strings overrides. Format: [ENTITY_TYPE] [REPLACEMENT_TEXT]"
)
@click.option(
    '--port', '-p', 
    type=int, 
    default=8420, 
    help="Network port to attach HTTP Stream server onto."
)
def run_cli(entity, token, port):
    """Execution CLI wrapper configuration for your PII Filter NextCloud MCP node."""
    entities_list = list(entity)
    tokens_dict = dict(token) if token else None
    
    click.echo(f"[*] Starting MCP Core Node on port {port}...")
    click.echo(f"[*] Monitoring Entities: {entities_list}")
    if tokens_dict:
        click.echo(f"[*] Custom replacement maps defined: {tokens_dict}")

    # Inject variables straight into global server states
    init_server(entities=entities_list, tokens=tokens_dict)
    
    # Run server instance
    mcp.run(transport="streamable-http")

if __name__ == '__main__':
    run_cli()
