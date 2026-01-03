# Lean Architecture Reference

Based on the ParkOptimizer project - a MATLAB wind farm optimization system demonstrating excellent OOP design.

---

## The Gold Standard: ParkOptimizer

ParkOptimizer achieves complex wind farm optimization with **12 focused domain classes**:

| Class | Purpose | LOC |
|-------|---------|-----|
| `cTurbine` | Wind turbine data (power curve, thrust) | ~112 |
| `cWeibull` | Wind distribution model | ~1,099 |
| `cLayout` | Turbine positioning optimization | ~200+ |
| `cParkDesign` | Project orchestrator | ~150 |
| `cGrid` | Spatial grid definition | ~100 |
| `cParkarea` | Park area boundaries | ~100 |
| `cEnergy` | Energy production calculations | ~150 |
| `cMeasurement` | Measurement data handling | ~100 |
| `cConstraints` | Layout constraints (IEC subtypes) | ~200 |
| `cMatrix` | Data matrix operations | ~100 |
| `cReportIEC` | IEC standard reporting | ~150 |
| `cHandle` | Base reference type | ~50 |

**Key insight**: Zero `*Manager`, `*Service`, `*Handler`, or `*Processor` classes.

---

## Metrics for Healthy Architecture

### Class Density
```
Healthy:  < 5 classes per KLOC
Warning:  5-10 classes per KLOC
Bloated:  > 10 classes per KLOC
```

ParkOptimizer: 12 classes / ~5 KLOC = **2.4 classes/KLOC** (excellent)

### Class Size
```
Healthy:  100-300 LOC average
Warning:  50-100 LOC average
Bloated:  < 50 LOC average (thin wrappers)
```

### Layer Depth
```
Healthy:  ≤ 3 layers (Controller → Model → Database)
Warning:  4 layers
Bloated:  5+ layers (Controller → Service → Repository → Model → Database)
```

### Import Depth
```
Healthy:  ≤ 3 levels (from app.models.user import User)
Warning:  4 levels
Bloated:  5+ levels (from app.services.user.handlers.auth.tokens import JWTHandler)
```

---

## Naming Rules

### Domain Nouns (GOOD)
Name classes after business/domain concepts:
- `User`, `Account`, `Invoice`
- `Turbine`, `Layout`, `Grid`
- `Measurement`, `Report`, `Constraint`
- `Order`, `Product`, `Customer`

### Architecture Nouns (BAD - REJECT)
Never use these suffixes:
- `*Manager` - Vague, what does "manage" mean?
- `*Service` - Catch-all for anything
- `*Handler` - Implies passive delegation
- `*Processor` - Could mean anything
- `*Coordinator` - Adds useless layer
- `*Factory` - Only if polymorphism truly needed
- `*Helper` / `*Utility` - Should be functions
- `*Wrapper` - Thin delegation layer

---

## Anti-Patterns to Avoid

### 1. Layer Tax
```python
# BAD: 4 layers for simple CRUD
class UserController:
    def create(self, request):
        return self.service.create_user(request)

class UserService:
    def create_user(self, request):
        return self.repository.save(request)

class UserRepository:
    def save(self, request):
        return self.model.create(**request)

class UserModel:
    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

# GOOD: Direct domain logic
class User:
    @classmethod
    def create(cls, **kwargs) -> 'User':
        return cls(**kwargs)

@app.post("/users")
def create_user(request: UserRequest) -> User:
    return User.create(**request.dict())
```

### 2. Thin Wrappers
```python
# BAD: 3 classes with ~25 LOC each
class UserValidator:
    def validate(self, data): ...

class UserSaver:
    def save(self, user): ...

class UserService:
    def __init__(self, validator, saver): ...

# GOOD: 1 class with ~75 LOC
class User:
    def validate(self) -> bool: ...
    def save(self) -> None: ...
```

### 3. Speculative Generality
```python
# BAD: Interface with one implementation
class IUserRepository(ABC):
    @abstractmethod
    def get(self, id): ...

class SQLUserRepository(IUserRepository):
    def get(self, id): ...

# GOOD: Just the implementation
class User:
    @classmethod
    def get(cls, user_id: str) -> 'User':
        return db.query(cls).filter_by(id=user_id).first()
```

### 4. Config Object Explosion
```python
# BAD: Nested config objects
class DatabaseConfig(BaseModel):
    host: str
    port: int
    ...

class CacheConfig(BaseModel):
    ...

class AppConfig(BaseModel):
    database: DatabaseConfig
    cache: CacheConfig
    ...

# GOOD: Simple environment-based config
import os

DATABASE_URL = os.environ["DATABASE_URL"]
CACHE_TTL = int(os.environ.get("CACHE_TTL", 300))
```

---

## The Golden Question

Before creating any class, ask:

> **"Would the ParkOptimizer developers add this class?"**

If the answer is "they'd just add a method to an existing domain class" - that's what you should do.

---

## Refactoring Checklist

When reviewing existing code:

- [ ] Count classes per KLOC (target: <5)
- [ ] Check for architecture nouns (reject all)
- [ ] Measure average class LOC (target: 100-300)
- [ ] Count layer depth (target: ≤3)
- [ ] Check import depth (target: ≤3)
- [ ] Look for thin wrappers (<50 LOC)
- [ ] Find unnecessary interfaces (single implementation)
- [ ] Identify config object bloat

---

## Quick Reference

| Question | Lean Answer |
|----------|-------------|
| How many classes for a feature? | As few as domain requires |
| What to name a class? | Domain noun (User, Invoice, Turbine) |
| How big should a class be? | 100-300 LOC of real logic |
| How many layers? | ≤3 (Controller → Model → DB) |
| When to create a new class? | When it represents a domain concept |
| When to add to existing class? | When it's related domain logic |

---

## Sources

- **ParkOptimizer**: ~/klauspython/ParkOptimizer (MATLAB reference)
- **Daniel Tenner**: [DHH is immortal](https://danieltenner.com/dhh-is-immortal-and-costs-200-m/)
- **DHH Philosophy**: Rails framework design principles
- **Marc Schmidt**: Twitter thread on Claude Code anti-patterns

---

*Last updated: 2026-01-03*
