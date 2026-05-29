<a id="readme-top"></a>

[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT TITLE -->
<br />
<div align="center">
  <h3 align="center">greenfish-webtools-mcp</h3>

  <p align="center">
    A lightweight MCP server that gives AI assistants real-time web search and URL reading — no API keys required.
    <br />
    <a href="https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

greenfish-webtools-mcp is a [Model Context Protocol](https://modelcontextprotocol.io) server that equips AI assistants with live web access. It exposes two tools: **web search** and **URL content extraction**.

The key design choice is that this server does not talk to any proprietary search API. Instead, it delegates all search work to your own [SearXNG](https://github.com/searxng/searxng) instance — a self-hosted, actively maintained meta-search engine that aggregates results from multiple search providers and exposes a stable JSON API that won't change or be deprecated without notice. You spin up SearXNG, this server connects to it and passes results straight to the model.

`greenfish_websearch` sends a query to SearXNG and returns a ranked, deduplicated list of results. `greenfish_fetch_url` fetches a specific page and returns its main readable content, stripped of navigation, ads, and boilerplate using [trafilatura](https://github.com/adbar/trafilatura).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- BUILT WITH -->
## Built With

[![Python][Python-shield]][Python-url]
[![SearXNG][SearXNG-shield]][SearXNG-url]
[![uv][uv-shield]][uv-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Before anything else, make sure you have **Python 3.10+** and **[uv](https://github.com/astral-sh/uv)** installed. You will also need a running SearXNG instance with JSON output enabled. The quickest way to get one is via Docker:

```sh
docker run -d --name searxng -p 1818:8080 searxng/searxng
```

After that, open the SearXNG admin interface, go to **Preferences → General**, and enable `json` as an output format. Alternatively, find `settings.yml` in the SearXNG container and add `json` to the `search.formats` list, then restart the container.

Now clone this repository and install the Python dependencies:

```sh
git clone https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP.git
cd greenfish-webtools-mcp
uv sync
```

That's it. No API keys, no accounts.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Register the server in your MCP client configuration file. The example below works for Claude Desktop and most other clients that accept the standard JSON format:

```json
{
  "mcpServers": {
    "greenfish-webtools": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/greenfish-webtools-mcp",
        "run",
        "app.py"
      ],
      "env": {
        "SEARXNG_URL": "http://127.0.0.1:1818/search"
      }
    }
  }
}
```

Replace `/path/to/greenfish-webtools-mcp` with the actual path to the cloned repository on your machine, and adjust `SEARXNG_URL` to match the address where your SearXNG instance is running. Once the MCP server starts, the AI assistant will have access to `greenfish_websearch` and `greenfish_fetch_url` automatically.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Support for additional SearXNG parameters (time range, search categories)
- [ ] Configurable result ranking and deduplication strategy
- [ ] Multi-language documentation

See the [open issues](https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/issues) for a full list of proposed features and known issues.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also open an issue with the tag "enhancement". Don't forget to give the project a star — thanks!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU GPLv3 License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP](https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This project would not exist without [SearXNG](https://github.com/searxng/searxng), which does all the actual search work. Thanks also to the authors of [FastMCP](https://github.com/jlowin/fastmcp), [trafilatura](https://github.com/adbar/trafilatura), and [httpx](https://github.com/encode/httpx).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[forks-shield]: https://img.shields.io/github/forks/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[forks-url]: https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/network/members
[stars-shield]: https://img.shields.io/github/stars/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[stars-url]: https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/stargazers
[issues-shield]: https://img.shields.io/github/issues/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[issues-url]: https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/issues
[license-shield]: https://img.shields.io/github/license/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[license-url]: https://github.com/https://github.com/DumbGreenFish/GreenFishWebtoolsMCP/blob/master/LICENSE
[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[SearXNG-shield]: https://img.shields.io/badge/SearXNG-3050B0?style=for-the-badge
[SearXNG-url]: https://github.com/searxng/searxng
[uv-shield]: https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge
[uv-url]: https://github.com/astral-sh/uv
