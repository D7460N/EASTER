// D7460N Data Pipeline - Combined
// Data → Structure projection pipeline for semantic HTML

// 01 - API Transport
function apiOnInput(url, options = {}) {
  return fetch(url, options)
    .then(r => r.json())
    .then(data => {
      console.log('apiOnInput: success');
      return data;
    })
    .catch(() => {
      console.error('apiOnInput: error');
      return null;
    });
}

// 02 - Normalize Payload
function normalizePayload(payload, schema = {}) {
  if (!payload) return null;
  return typeof schema.transform === 'function'
    ? schema.transform(payload)
    : payload;
}

// 03 - Require Payload
function requirePayload(payload, message = 'Payload missing or invalid') {
  if (payload == null) {
    console.error(message);
    return null;
  }
  return payload;
}

// 04 - Select Schema
function selectSchema(payload, schemas = {}) {
  // For EASTER JSON structure, check if it has documents array
  if (payload && Array.isArray(payload.documents)) {
    return schemas.primary;
  }
  
  return typeof schemas.match === 'function'
    ? schemas.match(payload)
    : null;
}

// 05 - Schemas
const schemas = {
  enterprise: {
    navigation: { intent: 'navigational' },
    primary: { intent: 'primary-content' },
    descriptive: { intent: 'descriptive' },
    ancillary: { intent: 'ancillary' },
    relational: { intent: 'relational' },
    enumerative: { intent: 'enumerative' },
    status: { intent: 'status' },
    instructional: { intent: 'instructional' },
    interaction: { intent: 'interactive-metadata' },
    administrative: { intent: 'administrative' },
    temporal: { intent: 'temporal' },
    identity: { intent: 'identity' }
  },
  domain: {},
  local: {}
};

// 06 - Intent Regions
const intentRegions = {
  navigational: ['nav'],
  'primary-content': ['main'],
  descriptive: ['header', 'section'],
  ancillary: ['aside'],
  relational: ['section', 'aside'],
  enumerative: ['section', 'main'],
  status: ['header', 'aside'],
  instructional: ['main', 'aside'],
  'interactive-metadata': ['nav', 'aside'],
  administrative: ['aside'],
  temporal: ['section'],
  identity: ['header']
};

// 07 - Insertion Rules
const insertionRules = {
  strategy: 'replace',
  order: 'preserve',
  limit: null
};

// 08 - Diagnostics
function logBoundary(status, boundary, scope = 'pipeline') {
  status
    ? console.log(`${scope}: passed ${boundary}`)
    : console.error(`${scope}: stopped ${boundary}`);
}

// 09 - Process Payload
function processPayload(payload, schemas, regions, rules) {
  const normalized = normalizePayload(payload);
  const valid = requirePayload(normalized);
  if (!valid) return null;

  const schema = selectSchema(valid, schemas);
  if (!schema) return null;

  // Extract documents array if it exists
  const data = valid.documents ? valid.documents : valid;

  return {
    data: Array.isArray(data) ? data : [data],
    intent: schema.intent,
    regions: regions[schema.intent] || [],
    rules
  };
}

// 10 - Tag Name Converter
function toTagName(key) {
  if (!key) return null;

  const words = key
    .replace(/[^a-zA-Z0-9]/g, '')
    .replace(/([a-z0-9])([A-Z])/g, '$1-$2')
    .toLowerCase()
    .split('-')
    .slice(0, 4);

  const name = words.join('-');
  return name.includes('-') && !name.startsWith('-') ? name : `${name}-`;
}

// 11 - Project Record
function projectRecord(record, row) {
  Object.entries(record).forEach(([key, value]) => {
    let tag;

    if (!key) {
      tag = 'no-key';
    } else {
      const normalized = toTagName(key);
      tag = normalized && !normalized.startsWith('-')
        ? normalized
        : 'invalid-key';
    }

    if (key && (value == null || value === '')) {
      tag = 'no-value';
    }

    const el = document.createElement(tag);
    if (value != null && value !== '') el.textContent = value;

    row.appendChild(el);
  });
}

// 12 - Project Collection
function projectCollection(plan, root) {
  if (!plan || !Array.isArray(plan.data)) {
    logBoundary(false, 'projectCollection:invalid-plan');
    return null;
  }

  logBoundary(true, 'projectCollection:collection-received');

  plan.regions.forEach(region => {
    const container = root.querySelector(`${region} ol`);
    if (!container) {
      logBoundary(false, `projectCollection:missing-container-${region}`);
      return;
    }

    logBoundary(true, `projectCollection:container-${region}`);

    if (plan.rules.strategy === 'replace') {
      container.replaceChildren();
    }

    plan.data.forEach(record => {
      const row = document.createElement('li');
      projectRecord(record, row);
      container.appendChild(row);
    });

    logBoundary(true, `projectCollection:projected-${region}`);
  });

  logBoundary(true, 'projectCollection:completed');
  return true;
}

// 13 - Insert Plan
function insertPlan(plan, root) {
  if (!plan) return null;

  plan.regions.forEach(region => {
    projectCollection(plan, root);
  });

  return true;
}

// 14 - Run Pipeline (Public Entry Point)
function runPipeline(url, root, options) {
  return apiOnInput(url, options)
    .then(payload => processPayload(payload, schemas.enterprise, intentRegions, insertionRules))
    .then(plan => insertPlan(plan, root));
}
