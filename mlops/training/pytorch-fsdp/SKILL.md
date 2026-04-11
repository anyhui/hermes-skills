---
name: pytorch-fsdp
description: Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP - parameter sharding, mixed precision, CPU offloading, FSDP2. Use when training large models on multiple GPUs, implementing distributed training, or debugging FSDP issues.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [torch>=2.0, transformers]
metadata:
  hermes:
    tags: [Distributed Training, PyTorch, FSDP, Data Parallel, Sharding, Mixed Precision, CPU Offloading, FSDP2, Large-Scale Training]

---

# PyTorch FSDP Skill

Fully Sharded Data Parallel training with PyTorch - distribute large models across multiple GPUs.

## When to Use

- Training models that don't fit on a single GPU
- Implementing distributed training
- Debugging FSDP issues
- Need parameter sharding, mixed precision, CPU offloading

## Quick Start

### 1. Initialize Process Group

```python
import torch
import torch.distributed as dist

dist.init_process_group(backend="nccl")
```

### 2. Basic FSDP Wrap

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.distributed.fsdp import ShardingStrategy

model = YourModel()
model = FSDP(
    model,
    sharding_strategy=ShardingStrategy.FULL_SHARD,
    device_id=torch.cuda.current_device()
)
```

### 3. Mixed Precision Training

```python
from torch.distributed.fsdp import MixedPrecision

mp = MixedPrecision(
    param_dtype=torch.float16,
    reduce_dtype=torch.float16,
    buffer_dtype=torch.float16
)
model = FSDP(model, mixed_precision=mp)
```

## Core Concepts

### Sharding Strategies

| Strategy | Memory | Communication | Use Case |
|----------|--------|---------------|----------|
| `FULL_SHARD` | Lowest | Higher | Large models, limited memory |
| `SHARD_GRAD_OP` | Medium | Medium | Balance memory/speed |
| `NO_SHARD` | Highest | Lowest | Small models, fast training |

### Key Features

- **Parameter Sharding**: Split parameters across GPUs
- **Gradient Sharding**: Reduce memory for gradients
- **CPU Offloading**: Move unused parameters to CPU
- **Mixed Precision**: FP16/BF16 training

## FSDP2 (PyTorch 2.2+)

```python
from torch.distributed._composable.fsdp import fully_shard

model = YourModel()
model = fully_shard(model)
```

FSDP2 offers:
- Simpler API
- Better performance
- Per-module sharding

## Common Patterns

### Checkpointing

```python
from torch.distributed.fsdp import StateDictType
from torch.distributed.fsdp import FullStateDictConfig

model = FSDP(
    model,
    state_dict_type=StateDictType.FULL_STATE_DICT,
    full_state_dict_config=FullStateDictConfig(rank0_only=True)
)
```

### Wrap Policy

```python
from torch.distributed.fsdp.wrap import size_based_auto_wrap_policy

model = FSDP(
    model,
    auto_wrap_policy=size_based_auto_wrap_policy,
    min_num_params=1_000_000
)
```

## Troubleshooting

### CUDA OOM
- Enable CPU offloading: `cpu_offload=CPUOffload(offload_params=True)`
- Reduce batch size or increase gradient accumulation
- Use activation checkpointing

### Hangs
- Check all ranks are running
- Verify NCCL backend is working
- Check network connectivity

### Wrong Results
- Ensure all ranks have same model initialization
- Check sharding strategy matches your needs
- Verify data loading is consistent

## References

- PyTorch FSDP Docs: https://pytorch.org/docs/stable/fsdp.html
- FSDP Tutorial: https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html