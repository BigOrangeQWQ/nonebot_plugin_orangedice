from nonebot import init, load_plugin
from tomllib import load


def get_project_name() -> str:
    with open("pyproject.toml", "rb") as f:
        return load(f)['project']['name']
    
def run_plugin_test(name: str) -> None:
    init(driver="~none")
    valid = load_plugin(name)
    if not valid:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    run_plugin_test(get_project_name())