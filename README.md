# Ubuntu Package Search + Package Data Processing Pipeline
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

The project is a two parter:
- Data processing pipeline for ubuntu packages data
- Information Retrieval System for ubuntu packages

## Project Structure
- docs: Reports for FEUP-M.EIC-PRI course (Faculty of Engineering of University of Porto)
- graphical-interface: web app for searching ubuntu packages
- pipeline: scripts and makefile for the collection and processing of the information used in the system
- search-system: underlying [SOLR](https://solr.apache.org/) system configurations and scripts

## Authors

| Name                        | E-Mail                   |
| --------------------------- | ------------------------ |
| Francisco Pinto de Oliveira | up201907361@edu.fe.up.pt |
| Marcelo Henriques Couto     | up201906086@edu.fe.up.pt |
| José Pedro Abreu Silva      | up201904775@edu.fe.up.pt |

## Usage

### Pipeline

To run the pipeline, you will need Make. Run:
```sh
make
```

### Search System

Run the startup script in /search-system:
```sh
./startup.sh
```

Install the dependencies of the backend (/backend directory) and run it (you will need node and npm):
```sh
npm i
npm run start
```

Install the dependencies of the frontend (/frontend directory) and run it (you will need node and npm):
```sh
npm i
npm run start
```

### Evaluation Scripts

To run the evaluation scripts (evaluate the performance of the search system by generating metrics and graphs):

```sh
cd search-system/evaluation
python main.py
```
