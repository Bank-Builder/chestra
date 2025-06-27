# Chestra Prompts

This directory contains prompts and specifications for generating external tools and integrations for Chestra.

## Files

### `v0_prompt.md`
**Purpose**: Concise, v0.io-optimized prompt for generating a visual workflow builder UI
**Use Case**: Copy and paste this content into v0.io to generate an n8n-style visual workflow builder for Chestra
**Key Features**:
- Drag-and-drop interface with React Flow
- Support for all Chestra plugins (start, end, http, cmd, df, changed)
- Real-time YAML generation and validation
- Import/export functionality

### `v0_ui_specification.md`
**Purpose**: Detailed technical specification for the Chestra workflow UI
**Use Case**: Reference document for detailed requirements, architecture, and implementation details
**Key Features**:
- Complete plugin specifications with all parameters
- Technical architecture and data structures
- UI/UX design requirements
- Advanced features and success criteria

## Usage

1. **For v0.io generation**: Use `v0_prompt.md` - copy the content and paste into v0.io
2. **For detailed requirements**: Reference `v0_ui_specification.md` for comprehensive specifications
3. **For custom implementations**: Use both files as reference for building Chestra integrations

## Generated UI Features

The UI generated from these prompts will provide:
- Visual workflow builder similar to n8n
- Support for all built-in Chestra plugins
- Real-time YAML generation
- Workflow validation and error feedback
- Import/export functionality
- Responsive design for desktop and mobile

## Example Workflows

The generated UI will support common workflow patterns:
- HTTP API calls and data processing
- File processing and monitoring
- System monitoring and alerting
- Data pipeline workflows 