from streamlit_agraph import Node
from streamlit_agraph.config import Config, ConfigBuilder


nodes = []

nodes.append( Node(id="Spiderman",
                   label="Peter Parker",
                   size=25,
                   shape="circularImage",
                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png")
            ) # includes **kwargs
nodes.append( Node(id="Captain_Marvel",
                   size=25,
                   shape="circularImage",
                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png")
            )

# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# 2. If your done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")
