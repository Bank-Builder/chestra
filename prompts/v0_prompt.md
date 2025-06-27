# Create an n8n-style Visual Workflow Builder for Chestra

## Project: Chestra Workflow UI
Build a drag-and-drop visual workflow builder similar to n8n that generates YAML files for Chestra, a Python-based workflow orchestrator.

## Core Features Required:

### 1. **Visual Workflow Canvas**
- Drag-and-drop interface with React Flow
- Node-based design where each node represents a Chestra plugin
- Connection lines showing task dependencies
- Zoom, pan, and multi-select functionality
- Real-time validation and error highlighting

### 2. **Plugin Nodes** (Create visual nodes for these Chestra plugins):

**Start Node** (Green circle)
- Outputs: `TRUE`
- No inputs required

**End Node** (Red circle)  
- Inputs: Any task outputs
- No outputs

**HTTP Node** (Blue rectangle)
- Outputs: `status_code`, `data`, `headers`, `json_data`, `url`
- Parameters: `url` (required), `method`, `headers`, `data`, `json`, `timeout`, `verify`, `allow_redirects`

**CMD Node** (Orange terminal icon)
- Outputs: Any variables set by command
- Parameters: `command` (required)
- Permissions: `can_execute_commands`

**DF Node** (Purple hard drive icon)
- Outputs: `MAIN_VOLUME`, `FREE_SPACE`
- Permissions: `can_view_system`

**Changed Node** (Teal eye icon)
- Outputs: `CHANGED`
- Parameters: `file` (required), `timeout`

### 3. **Node Configuration Panel**
- Plugin selection dropdown
- Parameter inputs (text, number, boolean, JSON)
- Input/output mapping
- Permission requirements display
- Real-time validation feedback

### 4. **YAML Generation**
- Real-time YAML preview as user builds workflow
- Export workflow as downloadable YAML file
- Import existing YAML workflows
- Validation to ensure YAML is valid for Chestra

### 5. **Layout**
- Left sidebar: Plugin palette with draggable nodes
- Center: Main workflow canvas
- Right sidebar: Node configuration panel  
- Top toolbar: Save, load, export, import buttons
- Bottom panel: YAML preview

## Technical Stack:
- **React/Next.js** with TypeScript
- **React Flow** for the visual workflow builder
- **Tailwind CSS** for styling
- **Zustand** for state management
- **js-yaml** for YAML generation

## YAML Output Format:
```yaml
workflow:
  name: "Workflow Name"
  tasks:
    - name: "task_name"
      plugin: "plugin_type"
      inputs: ["previous_task.OUTPUT"]
      outputs: ["OUTPUT1", "OUTPUT2"]
      params:
        param1: "value"
        param2: 42
```

## Example Workflows to Support:
1. **Simple HTTP API Call**: Start → HTTP (GET /api/data) → End
2. **File Processing**: Start → CMD (process file) → Changed (monitor) → End  
3. **System Monitoring**: Start → DF (check disk) → HTTP (send alert) → End
4. **Data Pipeline**: Start → HTTP (fetch) → CMD (transform) → HTTP (store) → End

## Key Requirements:
- Users should be able to create workflows without writing YAML
- Generated YAML must be valid for Chestra execution
- UI should be responsive and accessible
- Support for all built-in Chestra plugins
- Real-time validation and error feedback

Create a fully functional web application that allows users to visually design Chestra workflows and export them as YAML files. 