#!/usr/bin/env node
/*
 * ELK layered runner for BPMN layout adapter.
 * Input: JSON file path (argv[2])
 * Output: JSON to stdout
 */

const fs = require('fs');

function loadElk() {
  try {
    const ELK = require('elkjs/lib/elk.bundled.js');
    return new ELK();
  } catch (e1) {
    try {
      const ELK = require('elkjs');
      return new ELK();
    } catch (e2) {
      return null;
    }
  }
}

async function main() {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('missing input path');
    process.exit(2);
  }

  const elk = loadElk();
  if (!elk) {
    console.error('elkjs not found');
    process.exit(3);
  }

  const payload = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const direction = (payload.flow_dir || 'LR').toUpperCase() === 'TB' ? 'DOWN' : 'RIGHT';

  const graph = {
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': direction,
      'elk.spacing.nodeNode': '26',
      'elk.layered.spacing.nodeNodeBetweenLayers': '72',
      'elk.spacing.edgeNode': '18',
      'elk.edgeRouting': 'ORTHOGONAL'
    },
    children: payload.nodes.map((n) => ({
      id: n.id,
      width: n.width,
      height: n.height
    })),
    edges: payload.edges.map((e, i) => ({
      id: e.id || `e_${i}`,
      sources: [e.source],
      targets: [e.target]
    }))
  };

  const result = await elk.layout(graph);
  const out = {
    children: (result.children || []).map((c) => ({
      id: c.id,
      x: c.x || 0,
      y: c.y || 0,
      width: c.width || 0,
      height: c.height || 0
    }))
  };

  process.stdout.write(JSON.stringify(out));
}

main().catch((err) => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
