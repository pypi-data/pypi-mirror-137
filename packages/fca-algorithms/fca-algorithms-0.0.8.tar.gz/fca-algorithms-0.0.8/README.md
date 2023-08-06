# FCA utils

Module for FCA basics such as retrieving concepts, drawing a hasse diagram, etc

## Getting formal concepts

```python
from fca.api_models import Context

c = Context(O, A, I)
concepts = c.get_concepts(c)
```

## Getting association rules


```python
from fca.api_models import Context

c = Context(O, A, I)
c.solver.get_association_rules(c, min_support=0.4, min_confidence=1)
```


## Drawing hasse diagram


```python
from fca.plot.plot import plot_from_hasse
from fca.api_models import Context


c = Context(O, A, I)
hasse_lattice, concepts = c.get_lattice(c)
plot_from_hasse(hasse_lattice, concepts)
```



# TODO

- Make algorithms to be able to work with streams (big files)

