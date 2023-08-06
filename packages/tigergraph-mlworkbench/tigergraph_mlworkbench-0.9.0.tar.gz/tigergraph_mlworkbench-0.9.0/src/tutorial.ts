import { Widget } from '@lumino/widgets';

type tutorialType = {
  [key: string]: {
    [key: string]: string;
  };
};

const tutorialIndex: { [key: string]: tutorialType } = {
  basics: {
    '0_data_ingestion': {
      label: 'Data Ingestion',
      url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/0_data_ingestion.ipynb'
    },
    '1_data_processing': {
      label: 'Data Processing',
      url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/1_data_processing.ipynb'
    },
    '2_dataloaders': {
      label: 'Data loaders',
      url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/2_dataloaders.ipynb'
    },
    '3.1_graph_convolutional_network': {
      label: 'Graph Convolutional Network',
      url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/3.1_graph_convolutional_network.ipynb'
    },
    '3.2_graphSAGE': {
      label: 'GraphSAGE',
      url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/3.2_graphSAGE.ipynb'
    },
    '3.3_graph_attention_network': {
      label: 'Graph Attention Network',
      url: 'https://raw.githubusercontent.com/tg-bill/mlworkbench-docs/main/tutorials/basics/3.3_graph_attention_network.ipynb'
    }
  }
};

export class MLTutorials extends Widget {
  public constructor() {
    const body = document.createElement('div');
    const label = document.createElement('label');
    label.textContent = 'Tutorials:';

    const tutoSelect = document.createElement('select');
    const basics = tutorialIndex.basics;
    for (const tid of Object.keys(basics)) {
      const option = document.createElement('option');
      option.label = basics[tid].label;
      option.text = basics[tid].label;
      option.value = basics[tid].url;
      tutoSelect.appendChild(option);
    }

    body.appendChild(label);
    body.appendChild(tutoSelect);
    super({ node: body });
  }

  public getValue(): string {
    return this.inputNode.value;
  }

  public get inputNode(): HTMLSelectElement {
    return this.node.getElementsByTagName('select')[0];
  }
}
