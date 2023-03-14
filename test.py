from nonebot import init, load_plugin

try:
    from tomllib import loads as load
except:
    from tomlkit import parse as load
    


def get_project_name() -> str:
    with open("pyproject.toml", "r") as f:
        return load(f.read()).get("project", {}).get("name", "noneplugin")
    
def run_plugin_test(name: str) -> None:
    init(driver="~none")
    valid = load_plugin(name)
    if not valid:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    run_plugin_test(get_project_name())