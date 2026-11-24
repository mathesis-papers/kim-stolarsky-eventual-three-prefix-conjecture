# Kim–Stolarsky's eventual three-prefix conjecture

The note gives corrected continued-fraction prefixes for all three odd root
branches, proves their ordering and all three limiting digit ratios, and
determines full rational expansions for the squared odd and even terms.
It also answers the posing authors' double-zero-separation question by
specializing their own displayed identity.

## Contents and build

- `note.tex`: the mathematical note with its bibliography.
- `note.pdf` (supplied separately): the typeset note.
- `metadata.json`: scientific coverage, creators and license.
- `verify.py`: exact-arithmetic checks using the Python 3 standard library.
- `checker-output.json`: the deterministic checker output.

From the extracted source directory, run:

```sh
tectonic note.tex
python3 verify.py > regenerated-checker-output.json
cmp checker-output.json regenerated-checker-output.json
```

Use Tectonic 0.17.0. Alternatively, run `pdflatex note.tex` twice.
The bibliography is included directly, so BibTeX is unnecessary.
The source is self-contained and needs no network access to scientific inputs.
A TeX installation may retrieve its ordinary typesetting packages.

## Mathematical coverage

For `m=10^(4n+2)`, `n>=1`, the original L prefix holds. The corrected R third
digit is `floor((m-3)/7)`, and the corrected Q fourth digit is
`floor((6m+128)/35)`. Both original R and Q prefixes fail exactly for
`n=2 mod 3`. The negative roots satisfy `y_R>y_L>y_Q>4`; the three digit-ratio
limits are `101/3`, `7/2`, and `35/8`.

The all-parameter results have complete written proofs in the note.
The checker compares polynomial coefficients and exact rational sign bounds;
it also checks the full squared-root expansions for `n=0..60`, cubic prefix
brackets for `n=1..60`, the stated general even-parameter ranges through
`m=10000`, and small source-sum and double-zero-family controls. It uses
unbounded integers and `fractions.Fraction`, without floating-point rounding.
The finite controls are distinct from the written proofs.

The posing source is Seon-Hong Kim and Kenneth B. Stolarsky,
*A balanced three or more-term generalization of Nicomachus' identity*,
Integers 26 (2026), A98, Theorem 1, p. 5 and Remark 3, p. 6;
<https://doi.org/10.5281/zenodo.21678529>.
The preprint locator is arXiv:2511.15133v1, Remark 4, p. 6.
The double-zero question and the identity giving its answer are on journal p. 4.

The pinned Lean declaration
[`KimStolarskyEventualPrefixRefutation.result`](https://github.com/the-omega-institute/trureturing/blob/53c631a19a8292b44b6ed47b8cb236f00c7f5ed8/D5/S1/Depth/ContinuedFractions/KimStolarskyEventualPrefixRefutation.lean)
has conclusion the negation of the original simultaneous eventual assertion.
Its definition of complete quotients comes from
[`QuadraticImpliesPeriodic.completeQuotient`](https://github.com/the-omega-institute/trureturing/blob/53c631a19a8292b44b6ed47b8cb236f00c7f5ed8/D5/S1/Depth/ContinuedFractions/QuadraticImpliesPeriodic.lean).
The additional corrected prefixes, full expansions, ordering, ratio limits
and double-zero consequence are established by the written proofs, not
additional conclusions of that declaration. No periodicity theorem is needed.

## Creators and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
