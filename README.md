# machine-learning-labs
Machine learning with 

## Topic Modules

### Self-Attention Variants

- Overview: `self-attention-variants/README.md`
- Basic concepts: `self-attention-variants/basic.md`
- Basic code notebook: `self-attention-variants/basic.ipynb`
- Advanced concepts: `self-attention-variants/advanced.md`
- Advanced code notebook: `self-attention-variants/advanced.ipynb`

### Vulnerability Defenses

- Overview: `vulnerability-defenses/README.md`
- Input validation and sanitization: `vulnerability-defenses/input-validation-sanitization.md`
- Authentication and authorization hardening: `vulnerability-defenses/authn-authz-hardening.md`
- Secret and data protection: `vulnerability-defenses/secret-data-protection.md`
- Dependency and supply chain protection: `vulnerability-defenses/dependency-supply-chain-protection.md`
- Runtime and infrastructure hardening: `vulnerability-defenses/runtime-infrastructure-hardening.md`
- Monitoring and response readiness: `vulnerability-defenses/monitoring-response-readiness.md`

## Runtime Device Config

Use the project-level runtime flag file to switch GPU/CPU behavior:

- Template: `configs/runtime.env.example`
- Active config: `configs/runtime.env`
- `USE_GPU=1` => GPU mode (default)
- `USE_GPU=0` => CPU fallback

Foundation and PEFT notebooks automatically load `configs/runtime.env` (fallback: `configs/runtime.env.example`) and map `USE_GPU` to runtime device selection.

Quick switch:

1. Open `configs/runtime.env`
2. Set `USE_GPU=1` for GPU-first mode or `USE_GPU=0` to force CPU
3. Re-run the notebook from the first code cell
