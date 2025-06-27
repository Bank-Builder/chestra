# Chestra Workflow UI Specification for v0.io

## Project Overview
Create an n8n-style visual workflow builder for **Chestra**, a Python-based workflow orchestrator. The UI should allow users to visually design workflows that generate YAML files compatible with Chestra's execution engine.

## Core Requirements

### 1. **Visual Workflow Builder (n8n-style)**
- **Drag-and-drop interface** for adding and connecting tasks
- **Node-based design** where each node represents a Chestra plugin
- **Connection lines** showing task dependencies and data flow
- **Real-time validation** of workflow structure
- **Zoom and pan** functionality for large workflows

### 2. **Plugin Node Types**
Create visual nodes for all built-in Chestra plugins:

#### **Start Plugin**
- **Purpose**: Workflow initialization
- **Outputs**: `TRUE` (always outputs "1")
- **Visual**: Green circle with "START" label
- **No inputs required**

#### **End Plugin**
- **Purpose**: Workflow completion
- **Inputs**: Any task outputs
- **Visual**: Red circle with "END" label
- **No outputs**

#### **HTTP Plugin**
- **Purpose**: Make HTTP requests
- **Inputs**: Optional (from previous tasks)
- **Outputs**: `status_code`, `data`, `headers`, `json_data`, `url`
- **Parameters**:
  - `url` (required): Target URL
  - `method`: HTTP method (GET, POST, PUT, DELETE, etc.)
  - `headers`: Key-value pairs for HTTP headers
  - `data`: Request body data
  - `json`: JSON payload
  - `timeout`: Request timeout in seconds
  - `verify`: SSL certificate verification
  - `allow_redirects`: Follow redirects
- **Visual**: Blue rectangle with HTTP icon

#### **CMD Plugin**
- **Purpose**: Execute shell commands
- **Inputs**: Optional (from previous tasks)
- **Outputs**: Any variables set by the command
- **Parameters**:
  - `command` (required): Shell command to execute
- **Visual**: Terminal icon with "CMD" label
- **Permissions**: Requires `can_execute_commands`

#### **DF Plugin**
- **Purpose**: Get disk space information
- **Inputs**: Optional (from previous tasks)
- **Outputs**: `MAIN_VOLUME`, `FREE_SPACE`
- **Parameters**: None
- **Visual**: Hard drive icon with "DF" label
- **Permissions**: Requires `can_view_system`

#### **Changed Plugin**
- **Purpose**: Monitor file changes
- **Inputs**: Optional (from previous tasks)
- **Outputs**: `CHANGED` (boolean)
- **Parameters**:
  - `file` (required): File path to monitor
  - `timeout`: Monitoring timeout in seconds
- **Visual**: Eye icon with "CHANGED" label

### 3. **Node Configuration Panel**
Each node should have a configuration panel with:
- **Plugin selection** dropdown
- **Parameter inputs** (text, number, boolean, JSON)
- **Input mapping** (connect to previous task outputs)
- **Output selection** (choose which outputs to expose)
- **Permission requirements** (if applicable)
- **Validation feedback** (real-time error checking)

### 4. **Data Flow Visualization**
- **Input/Output mapping**: Show how data flows between tasks
- **Variable substitution**: Display `$TASK.OUTPUT` format
- **Environment variables**: Show available variables from previous tasks
- **Type indicators**: Visual cues for different data types

### 5. **YAML Generation**
- **Real-time YAML preview**: Show generated YAML as user builds workflow
- **Export functionality**: Download workflow as YAML file
- **Import functionality**: Load existing YAML workflows
- **Validation**: Ensure generated YAML is valid for Chestra

### 6. **Workflow Management**
- **Save/Load**: Save workflows to browser storage or file system
- **Templates**: Pre-built workflow templates
- **Versioning**: Track workflow changes
- **Sharing**: Export/import workflows between users

## Technical Specifications

### **Frontend Technology**
- **React/Next.js** for the main application
- **React Flow** or **D3.js** for the visual workflow builder
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Zod** for validation

### **State Management**
- **Zustand** or **Redux Toolkit** for workflow state
- **React Query** for any API calls
- **Local storage** for workflow persistence

### **Data Structure**
```typescript
interface WorkflowNode {
  id: string;
  type: 'start' | 'end' | 'http' | 'cmd' | 'df' | 'changed' | 'custom';
  position: { x: number; y: number };
  data: {
    name: string;
    plugin: string;
    inputs: string[];
    outputs: string[];
    params: Record<string, any>;
    requires_auth: boolean;
    permissions: string[];
  };
}

interface WorkflowConnection {
  id: string;
  source: string;
  target: string;
  sourceHandle: string;
  targetHandle: string;
}

interface Workflow {
  name: string;
  nodes: WorkflowNode[];
  edges: WorkflowConnection[];
}
```

### **YAML Generation Logic**
```typescript
function generateYAML(workflow: Workflow): string {
  const tasks = workflow.nodes.map(node => ({
    name: node.data.name,
    plugin: node.data.plugin,
    inputs: node.data.inputs,
    outputs: node.data.outputs,
    params: node.data.params,
    requires_auth: node.data.requires_auth,
    permissions: node.data.permissions
  }));

  return yaml.dump({
    workflow: {
      name: workflow.name,
      tasks: tasks
    }
  });
}
```

## UI/UX Design Requirements

### **Color Scheme**
- **Start nodes**: Green (#10B981)
- **End nodes**: Red (#EF4444)
- **HTTP nodes**: Blue (#3B82F6)
- **CMD nodes**: Orange (#F59E0B)
- **DF nodes**: Purple (#8B5CF6)
- **Changed nodes**: Teal (#14B8A6)
- **Custom nodes**: Gray (#6B7280)

### **Layout**
- **Left sidebar**: Plugin palette with draggable nodes
- **Center**: Main workflow canvas
- **Right sidebar**: Node configuration panel
- **Top toolbar**: Save, load, export, import, run buttons
- **Bottom panel**: YAML preview and validation messages

### **Responsive Design**
- **Desktop-first**: Optimized for large screens
- **Tablet support**: Collapsible sidebars
- **Mobile**: Simplified view with list-based workflow builder

## Advanced Features

### **1. Workflow Validation**
- **Real-time validation**: Check for cycles, missing inputs, invalid connections
- **Error highlighting**: Visual indicators for problematic nodes
- **Suggestions**: Auto-suggest fixes for common issues

### **2. Template System**
- **Built-in templates**: Common workflow patterns
- **Custom templates**: User-defined reusable workflows
- **Template marketplace**: Community-shared templates

### **3. Execution Integration**
- **Test execution**: Run workflows directly from UI
- **Execution status**: Real-time status updates
- **Log viewing**: Display execution logs
- **Error reporting**: Show detailed error information

### **4. Plugin Development**
- **Custom plugin builder**: Visual plugin creation
- **Plugin testing**: Test plugins within the UI
- **Plugin documentation**: Auto-generated docs from plugin code

## Example Workflows to Include

### **1. Simple HTTP API Call**
```
Start → HTTP (GET /api/data) → End
```

### **2. File Processing Pipeline**
```
Start → CMD (process file) → Changed (monitor output) → End
```

### **3. System Monitoring**
```
Start → DF (check disk) → HTTP (send alert) → End
```

### **4. Data Pipeline**
```
Start → HTTP (fetch data) → CMD (transform) → HTTP (store) → End
```

## Success Criteria

1. **Usability**: Users can create workflows without writing YAML
2. **Accuracy**: Generated YAML executes correctly in Chestra
3. **Performance**: UI remains responsive with large workflows
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Extensibility**: Easy to add new plugin types

## Deliverables

1. **Working UI application** with all core features
2. **YAML generation** that produces valid Chestra workflows
3. **Documentation** for users and developers
4. **Example workflows** demonstrating all plugin types
5. **Testing suite** for validation and edge cases

This UI will make Chestra accessible to non-technical users while maintaining the power and flexibility of the underlying orchestration engine. 