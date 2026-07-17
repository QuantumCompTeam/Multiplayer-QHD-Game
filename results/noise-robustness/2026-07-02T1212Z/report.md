# Experiment report: noise-robustness

RQ3: quantum advantage under a depolarizing channel (p on u, p on cx in the pinned {u, cx} basis) for GHZ / W / ring, N = 2..5, V=4, C=3, gamma=pi/2. W results approximate (transpiled-unitary entangler, spec D2).

_Generated: 2026-07-02T1212Z_

## Parameters used

```yaml
experiment:
  name: noise-robustness
  description: 'RQ3: quantum advantage under a depolarizing channel (p on u, p on
    cx in the pinned {u, cx} basis) for GHZ / W / ring, N = 2..5, V=4, C=3, gamma=pi/2.
    W results approximate (transpiled-unitary entangler, spec D2).'
generated_at: 2026-07-02T1212Z
output:
  formats:
  - md
  - json
  - csv
  - plots
cells:
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 2
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 2
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 2
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 3
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 3
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 3
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 4
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 4
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 4
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 5
  topology: ghz
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 5
  topology: w
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.0
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.005
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.01
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.015
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.02
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.025
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.03
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.035
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.04
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.045
- N: 5
  topology: ring
  strategy_names:
  - D
  - H
  - Q
  V: 4.0
  C: 3.0
  gamma: 1.5707963267948966
  gamma_label: pi/2
  strategy_mode: fixed
  noise_p: 0.05
```

## Summary

| N | topology | V | C | gamma | noise_p | q_payoff | classical_ne | advantage | q_is_nash | symmetric | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | ghz | 4 | 3 | pi/2 | 0 | 2.000000 | 0.500000 | 1.500000 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.005 | 1.974586 | 0.576241 | 1.398345 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.01 | 1.950780 | 0.647661 | 1.303119 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.015 | 1.928486 | 0.714542 | 1.213944 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.02 | 1.907616 | 0.777153 | 1.130463 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.025 | 1.888085 | 0.835745 | 1.052340 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.03 | 1.869814 | 0.890559 | 0.979254 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.035 | 1.852727 | 0.941820 | 0.910906 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.04 | 1.836752 | 0.989743 | 0.847010 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.045 | 1.821824 | 1.034527 | 0.787297 | yes | yes | ok |
| 2 | ghz | 4 | 3 | pi/2 | 0.05 | 1.807878 | 1.076366 | 0.731512 | yes | yes | ok |
| 2 | w | 4 | 3 | pi/2 | 0 | 2.000000 | 1.250000 | 0.750000 | **NO** | yes | ok |
| 2 | w | 4 | 3 | pi/2 | 0.005 | 1.967299 | 1.281800 | 0.685499 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.01 | 1.937318 | 1.311018 | 0.626300 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.015 | 1.909840 | 1.337855 | 0.571985 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.02 | 1.884668 | 1.362497 | 0.522171 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.025 | 1.861616 | 1.385116 | 0.476500 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.03 | 1.840515 | 1.405872 | 0.434643 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.035 | 1.821208 | 1.424912 | 0.396296 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.04 | 1.803548 | 1.442371 | 0.361178 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.045 | 1.787404 | 1.458374 | 0.329029 | **NO** | no | ok |
| 2 | w | 4 | 3 | pi/2 | 0.05 | 1.772650 | 1.473039 | 0.299611 | **NO** | no | ok |
| 2 | ring | 4 | 3 | pi/2 | 0 | 2.000000 | 0.500000 | 1.500000 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.005 | 1.974586 | 0.576241 | 1.398345 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.01 | 1.950780 | 0.647661 | 1.303119 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.015 | 1.928486 | 0.714542 | 1.213944 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.02 | 1.907616 | 0.777153 | 1.130463 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.025 | 1.888085 | 0.835745 | 1.052340 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.03 | 1.869814 | 0.890559 | 0.979254 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.035 | 1.852727 | 0.941820 | 0.910906 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.04 | 1.836752 | 0.989743 | 0.847010 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.045 | 1.821824 | 1.034527 | 0.787297 | yes | yes | ok |
| 2 | ring | 4 | 3 | pi/2 | 0.05 | 1.807878 | 1.076366 | 0.731512 | yes | yes | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0 | 1.333333 | 0.333333 | 1.000000 | yes | yes | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.005 | 1.312297 | 0.414429 | 0.897868 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.01 | 1.293970 | 0.488181 | 0.805789 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.015 | 1.278050 | 0.555238 | 0.722812 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.02 | 1.264263 | 0.616193 | 0.648070 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.025 | 1.252366 | 0.671590 | 0.580776 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.03 | 1.242139 | 0.721922 | 0.520217 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.035 | 1.233386 | 0.767644 | 0.465742 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.04 | 1.225931 | 0.809166 | 0.416765 | yes | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.045 | 1.219616 | 0.846866 | 0.372750 | **NO** | no | ok |
| 3 | ghz | 4 | 3 | pi/2 | 0.05 | 1.214302 | 0.881087 | 0.333215 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0 | 1.333333 | 0.833333 | 0.500000 | **NO** | yes | ok |
| 3 | w | 4 | 3 | pi/2 | 0.005 | 1.301953 | 0.948943 | 0.353010 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.01 | 1.278510 | 1.028511 | 0.249999 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.015 | 1.260903 | 1.083424 | 0.177479 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.02 | 1.247646 | 1.121418 | 0.126229 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.025 | 1.237661 | 1.147766 | 0.089895 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.03 | 1.230147 | 1.166075 | 0.064072 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.035 | 1.224506 | 1.178821 | 0.045685 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.04 | 1.220283 | 1.187707 | 0.032575 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.045 | 1.217131 | 1.193911 | 0.023221 | **NO** | no | ok |
| 3 | w | 4 | 3 | pi/2 | 0.05 | 1.214788 | 1.198246 | 0.016543 | **NO** | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0 | 1.333333 | 0.333333 | 1.000000 | yes | yes | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.005 | 1.315229 | 0.461853 | 0.853376 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.01 | 1.299708 | 0.571856 | 0.727852 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.015 | 1.286408 | 0.665956 | 0.620451 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.02 | 1.275016 | 0.746405 | 0.528610 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.025 | 1.265262 | 0.815144 | 0.450118 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.03 | 1.256916 | 0.873843 | 0.383073 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.035 | 1.249776 | 0.923939 | 0.325837 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.04 | 1.243672 | 0.966669 | 0.277003 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.045 | 1.238454 | 1.003094 | 0.235360 | yes | no | ok |
| 3 | ring | 4 | 3 | pi/2 | 0.05 | 1.233997 | 1.034127 | 0.199870 | yes | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0 | 1.000000 | 0.250000 | 0.750000 | **NO** | yes | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.005 | 0.981314 | 0.332747 | 0.648568 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.01 | 0.966116 | 0.405610 | 0.560507 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.015 | 0.953881 | 0.469779 | 0.484101 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.02 | 0.944152 | 0.976333 | -0.032182 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.025 | 0.936536 | 0.972772 | -0.036235 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.03 | 0.930695 | 0.969853 | -0.039157 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.035 | 0.926337 | 0.967466 | -0.041129 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.04 | 0.923212 | 0.965519 | -0.042307 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.045 | 0.921105 | 0.963934 | -0.042829 | **NO** | no | ok |
| 4 | ghz | 4 | 3 | pi/2 | 0.05 | 0.919833 | 0.962644 | -0.042811 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0 | 1.000000 | 0.625000 | 0.375000 | **NO** | yes | ok |
| 4 | w | 4 | 3 | pi/2 | 0.005 | 0.967165 | 0.892613 | 0.074552 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.01 | 0.957006 | 0.940498 | 0.016508 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.015 | 0.954180 | 0.950189 | 0.003992 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.02 | 0.953414 | 0.952383 | 0.001031 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.025 | 0.953205 | 0.952927 | 0.000279 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.03 | 0.953148 | 0.953070 | 0.000078 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.035 | 0.953132 | 0.953109 | 0.000022 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.04 | 0.953127 | 0.953123 | 0.000004 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.045 | 0.953126 | 0.953124 | 0.000001 | **NO** | no | ok |
| 4 | w | 4 | 3 | pi/2 | 0.05 | 0.953125 | 0.953125 | 0.000000 | **NO** | yes | ok |
| 4 | ring | 4 | 3 | pi/2 | 0 | 0.250000 | 0.250000 | 0.000000 | **NO** | yes | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.005 | 0.376895 | 0.376688 | 0.000207 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.01 | 0.481231 | 0.480534 | 0.000697 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.015 | 0.566955 | 0.565637 | 0.001318 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.02 | 0.637337 | 0.635368 | 0.001970 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.025 | 0.695081 | 0.692495 | 0.002586 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.03 | 0.742420 | 0.739293 | 0.003127 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.035 | 0.781201 | 0.777628 | 0.003573 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.04 | 0.812948 | 0.809031 | 0.003917 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.045 | 0.838917 | 0.834759 | 0.004158 | **NO** | no | ok |
| 4 | ring | 4 | 3 | pi/2 | 0.05 | 0.860145 | 0.855841 | 0.004304 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0 | 0.800000 | 0.200000 | 0.600000 | **NO** | yes | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.005 | 0.782889 | 0.283165 | 0.499724 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.01 | 0.769944 | 0.789418 | -0.019474 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.015 | 0.760363 | 0.786037 | -0.025673 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.02 | 0.753486 | 0.783459 | -0.029973 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.025 | 0.748765 | 0.781571 | -0.032806 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.03 | 0.745753 | 0.780225 | -0.034472 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.035 | 0.744080 | 0.779298 | -0.035218 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.04 | 0.743446 | 0.778694 | -0.035248 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.045 | 0.743607 | 0.778334 | -0.034727 | **NO** | no | ok |
| 5 | ghz | 4 | 3 | pi/2 | 0.05 | 0.744364 | 0.778158 | -0.033793 | **NO** | no | ok |
| 5 | w | 4 | 3 | pi/2 | 0 | 0.800000 | 0.500000 | 0.300000 | **NO** | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.005 | 0.781498 | 0.780315 | 0.001183 | **NO** | no | ok |
| 5 | w | 4 | 3 | pi/2 | 0.01 | 0.781255 | 0.781244 | 0.000011 | **NO** | no | ok |
| 5 | w | 4 | 3 | pi/2 | 0.015 | 0.781250 | 0.781250 | 0.000000 | **NO** | no | ok |
| 5 | w | 4 | 3 | pi/2 | 0.02 | 0.781250 | 0.781250 | 0.000000 | **NO** | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.025 | 0.781250 | 0.781250 | 0.000000 | **NO** | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.03 | 0.781250 | 0.781250 | -0.000000 | yes | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.035 | 0.781250 | 0.781250 | -0.000000 | yes | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.04 | 0.781250 | 0.781250 | -0.000000 | yes | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.045 | 0.781250 | 0.781250 | -0.000000 | yes | yes | ok |
| 5 | w | 4 | 3 | pi/2 | 0.05 | 0.781250 | 0.781250 | -0.000000 | yes | yes | ok |
| 5 | ring | 4 | 3 | pi/2 | 0 | 0.800000 | 0.200000 | 0.600000 | **NO** | yes | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.005 | 0.796221 | 0.323823 | 0.472398 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.01 | 0.793244 | 0.420919 | 0.372324 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.015 | 0.790893 | 0.497089 | 0.293804 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.02 | 0.789031 | 0.556873 | 0.232158 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.025 | 0.787553 | 0.603827 | 0.183726 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.03 | 0.786376 | 0.640734 | 0.145642 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.035 | 0.785434 | 0.669771 | 0.115664 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.04 | 0.784679 | 0.692640 | 0.092039 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.045 | 0.784071 | 0.710675 | 0.073396 | **NO** | no | ok |
| 5 | ring | 4 | 3 | pi/2 | 0.05 | 0.783579 | 0.724917 | 0.058662 | **NO** | no | ok |

## Findings

- Evaluated **132** cells: 132 ran, 0 not-implemented, 0 errored.
- Quantum advantage > 0 in **110/132** computed cells.
- (Q,...,Q) is a pure Nash equilibrium in **47/132** computed cells.

**Cells with advantage <= 0 (RQ1 finding — investigate, do not paper over):**
  - N=4, ghz, gamma=pi/2, p=0.02: advantage = -0.032182
  - N=4, ghz, gamma=pi/2, p=0.025: advantage = -0.036235
  - N=4, ghz, gamma=pi/2, p=0.03: advantage = -0.039157
  - N=4, ghz, gamma=pi/2, p=0.035: advantage = -0.041129
  - N=4, ghz, gamma=pi/2, p=0.04: advantage = -0.042307
  - N=4, ghz, gamma=pi/2, p=0.045: advantage = -0.042829
  - N=4, ghz, gamma=pi/2, p=0.05: advantage = -0.042811
  - N=4, ring, gamma=pi/2: advantage = 0.000000
  - N=5, ghz, gamma=pi/2, p=0.01: advantage = -0.019474
  - N=5, ghz, gamma=pi/2, p=0.015: advantage = -0.025673
  - N=5, ghz, gamma=pi/2, p=0.02: advantage = -0.029973
  - N=5, ghz, gamma=pi/2, p=0.025: advantage = -0.032806
  - N=5, ghz, gamma=pi/2, p=0.03: advantage = -0.034472
  - N=5, ghz, gamma=pi/2, p=0.035: advantage = -0.035218
  - N=5, ghz, gamma=pi/2, p=0.04: advantage = -0.035248
  - N=5, ghz, gamma=pi/2, p=0.045: advantage = -0.034727
  - N=5, ghz, gamma=pi/2, p=0.05: advantage = -0.033793
  - N=5, w, gamma=pi/2, p=0.03: advantage = -0.000000
  - N=5, w, gamma=pi/2, p=0.035: advantage = -0.000000
  - N=5, w, gamma=pi/2, p=0.04: advantage = -0.000000
  - N=5, w, gamma=pi/2, p=0.045: advantage = -0.000000
  - N=5, w, gamma=pi/2, p=0.05: advantage = -0.000000

**Cells where (Q,...,Q) is NOT Nash (RQ1 finding):**
  - N=2, w, gamma=pi/2
  - N=2, w, gamma=pi/2, p=0.005
  - N=2, w, gamma=pi/2, p=0.01
  - N=2, w, gamma=pi/2, p=0.015
  - N=2, w, gamma=pi/2, p=0.02
  - N=2, w, gamma=pi/2, p=0.025
  - N=2, w, gamma=pi/2, p=0.03
  - N=2, w, gamma=pi/2, p=0.035
  - N=2, w, gamma=pi/2, p=0.04
  - N=2, w, gamma=pi/2, p=0.045
  - N=2, w, gamma=pi/2, p=0.05
  - N=3, ghz, gamma=pi/2, p=0.045
  - N=3, ghz, gamma=pi/2, p=0.05
  - N=3, w, gamma=pi/2
  - N=3, w, gamma=pi/2, p=0.005
  - N=3, w, gamma=pi/2, p=0.01
  - N=3, w, gamma=pi/2, p=0.015
  - N=3, w, gamma=pi/2, p=0.02
  - N=3, w, gamma=pi/2, p=0.025
  - N=3, w, gamma=pi/2, p=0.03
  - N=3, w, gamma=pi/2, p=0.035
  - N=3, w, gamma=pi/2, p=0.04
  - N=3, w, gamma=pi/2, p=0.045
  - N=3, w, gamma=pi/2, p=0.05
  - N=4, ghz, gamma=pi/2
  - N=4, ghz, gamma=pi/2, p=0.005
  - N=4, ghz, gamma=pi/2, p=0.01
  - N=4, ghz, gamma=pi/2, p=0.015
  - N=4, ghz, gamma=pi/2, p=0.02
  - N=4, ghz, gamma=pi/2, p=0.025
  - N=4, ghz, gamma=pi/2, p=0.03
  - N=4, ghz, gamma=pi/2, p=0.035
  - N=4, ghz, gamma=pi/2, p=0.04
  - N=4, ghz, gamma=pi/2, p=0.045
  - N=4, ghz, gamma=pi/2, p=0.05
  - N=4, w, gamma=pi/2
  - N=4, w, gamma=pi/2, p=0.005
  - N=4, w, gamma=pi/2, p=0.01
  - N=4, w, gamma=pi/2, p=0.015
  - N=4, w, gamma=pi/2, p=0.02
  - N=4, w, gamma=pi/2, p=0.025
  - N=4, w, gamma=pi/2, p=0.03
  - N=4, w, gamma=pi/2, p=0.035
  - N=4, w, gamma=pi/2, p=0.04
  - N=4, w, gamma=pi/2, p=0.045
  - N=4, w, gamma=pi/2, p=0.05
  - N=4, ring, gamma=pi/2
  - N=4, ring, gamma=pi/2, p=0.005
  - N=4, ring, gamma=pi/2, p=0.01
  - N=4, ring, gamma=pi/2, p=0.015
  - N=4, ring, gamma=pi/2, p=0.02
  - N=4, ring, gamma=pi/2, p=0.025
  - N=4, ring, gamma=pi/2, p=0.03
  - N=4, ring, gamma=pi/2, p=0.035
  - N=4, ring, gamma=pi/2, p=0.04
  - N=4, ring, gamma=pi/2, p=0.045
  - N=4, ring, gamma=pi/2, p=0.05
  - N=5, ghz, gamma=pi/2
  - N=5, ghz, gamma=pi/2, p=0.005
  - N=5, ghz, gamma=pi/2, p=0.01
  - N=5, ghz, gamma=pi/2, p=0.015
  - N=5, ghz, gamma=pi/2, p=0.02
  - N=5, ghz, gamma=pi/2, p=0.025
  - N=5, ghz, gamma=pi/2, p=0.03
  - N=5, ghz, gamma=pi/2, p=0.035
  - N=5, ghz, gamma=pi/2, p=0.04
  - N=5, ghz, gamma=pi/2, p=0.045
  - N=5, ghz, gamma=pi/2, p=0.05
  - N=5, w, gamma=pi/2
  - N=5, w, gamma=pi/2, p=0.005
  - N=5, w, gamma=pi/2, p=0.01
  - N=5, w, gamma=pi/2, p=0.015
  - N=5, w, gamma=pi/2, p=0.02
  - N=5, w, gamma=pi/2, p=0.025
  - N=5, ring, gamma=pi/2
  - N=5, ring, gamma=pi/2, p=0.005
  - N=5, ring, gamma=pi/2, p=0.01
  - N=5, ring, gamma=pi/2, p=0.015
  - N=5, ring, gamma=pi/2, p=0.02
  - N=5, ring, gamma=pi/2, p=0.025
  - N=5, ring, gamma=pi/2, p=0.03
  - N=5, ring, gamma=pi/2, p=0.035
  - N=5, ring, gamma=pi/2, p=0.04
  - N=5, ring, gamma=pi/2, p=0.045
  - N=5, ring, gamma=pi/2, p=0.05

**Noise thresholds p\*** — smallest depolarizing p at which a series loses its quantum advantage (advantage ≤ 0, linearly interpolated between grid points) or (Q,…,Q) stops being a pure Nash equilibrium (True→False flip), whichever happens first. “> 0.05” = the advantage survived the whole swept grid (a finding, not a failure).

| topology | N | p* |
|---|---|---|
| ghz | 2 | > 0.05 |
| ghz | 3 | 0.0450 |
| ghz | 4 | 0.0197 † |
| ghz | 5 | 0.0098 † |
| ring | 2 | > 0.05 |
| ring | 3 | > 0.05 |
| ring | 4 | 0.0000 † |
| ring | 5 | > 0.05 † |
| w _(approximate)_ | 2 | > 0.05 † |
| w _(approximate)_ | 3 | > 0.05 † |
| w _(approximate)_ | 4 | > 0.05 † |
| w _(approximate)_ | 5 | 0.0294 |

† (Q,…,Q) is not a pure Nash equilibrium at ANY swept p for this series — with the fixed GHZ-derived Q this is a Month-3 finding about the topology, not noise fragility. The Nash-flip criterion is inert; p* reflects the advantage ≤ 0 criterion only.

**GHZ vs W noise robustness (RQ3 headline — measured, not assumed; W is approximate, see above):**
  - N=2: both survive the whole swept grid — no ordering measurable in range
  - N=3: GHZ collapses at p*=0.0450 while W survives the grid → GHZ degrades faster
  - N=4: GHZ collapses at p*=0.0197 while W survives the grid → GHZ degrades faster
  - N=5: GHZ collapses first (p*=0.0098 < 0.0294) → GHZ degrades faster

## Plots

![advantage_vs_N.png](plots/advantage_vs_N.png)
![noise/advantage_surface_ghz.png](plots/noise/advantage_surface_ghz.png)
![noise/advantage_surface_ring.png](plots/noise/advantage_surface_ring.png)
![noise/advantage_surface_w.png](plots/noise/advantage_surface_w.png)

## Per-cell detail

### N=2 · ghz · gamma=pi/2 (V=4, C=3)

- (Q,Q) mean per-player payoff: **2.000000**
- Classical NE mean payoff: **0.500000**
- Advantage (QNE − CNE, mean): **1.500000**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.500000 | 2.000000 | yes |
| player 0 | H | 0.000000 | 2.000000 | yes |
| player 1 | D | 0.500000 | 2.000000 | yes |
| player 1 | H | 0.000000 | 2.000000 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.974586**
- Classical NE mean payoff: **0.576241**
- Advantage (QNE − CNE, mean): **1.398345**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.570971 | 1.974586 | yes |
| player 0 | H | 0.110126 | 1.974586 | yes |
| player 1 | D | 0.570971 | 1.974586 | yes |
| player 1 | H | 0.110126 | 1.974586 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.950780**
- Classical NE mean payoff: **0.647661**
- Advantage (QNE − CNE, mean): **1.303119**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.637789 | 1.950780 | yes |
| player 0 | H | 0.213288 | 1.950780 | yes |
| player 1 | D | 0.637789 | 1.950780 | yes |
| player 1 | H | 0.213288 | 1.950780 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.928486**
- Classical NE mean payoff: **0.714542**
- Advantage (QNE − CNE, mean): **1.213944**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.700678 | 1.928486 | yes |
| player 0 | H | 0.309895 | 1.928486 | yes |
| player 1 | D | 0.700678 | 1.928486 | yes |
| player 1 | H | 0.309895 | 1.928486 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.907616**
- Classical NE mean payoff: **0.777153**
- Advantage (QNE − CNE, mean): **1.130463**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.759850 | 1.907616 | yes |
| player 0 | H | 0.400332 | 1.907616 | yes |
| player 1 | D | 0.759850 | 1.907616 | yes |
| player 1 | H | 0.400332 | 1.907616 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.888085**
- Classical NE mean payoff: **0.835745**
- Advantage (QNE − CNE, mean): **1.052340**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.815508 | 1.888085 | yes |
| player 0 | H | 0.484966 | 1.888085 | yes |
| player 1 | D | 0.815508 | 1.888085 | yes |
| player 1 | H | 0.484966 | 1.888085 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.869814**
- Classical NE mean payoff: **0.890559**
- Advantage (QNE − CNE, mean): **0.979254**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.867845 | 1.869814 | yes |
| player 0 | H | 0.564141 | 1.869814 | yes |
| player 1 | D | 0.867845 | 1.869814 | yes |
| player 1 | H | 0.564141 | 1.869814 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.852727**
- Classical NE mean payoff: **0.941820**
- Advantage (QNE − CNE, mean): **0.910906**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.917042 | 1.852727 | yes |
| player 0 | H | 0.638185 | 1.852727 | yes |
| player 1 | D | 0.917042 | 1.852727 | yes |
| player 1 | H | 0.638185 | 1.852727 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.836752**
- Classical NE mean payoff: **0.989743**
- Advantage (QNE − CNE, mean): **0.847010**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.963273 | 1.836752 | yes |
| player 0 | H | 0.707406 | 1.836752 | yes |
| player 1 | D | 0.963273 | 1.836752 | yes |
| player 1 | H | 0.707406 | 1.836752 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.821824**
- Classical NE mean payoff: **1.034527**
- Advantage (QNE − CNE, mean): **0.787297**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.006704 | 1.821824 | yes |
| player 0 | H | 0.772095 | 1.821824 | yes |
| player 1 | D | 1.006704 | 1.821824 | yes |
| player 1 | H | 0.772095 | 1.821824 | yes |

### N=2 · ghz · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.807878**
- Classical NE mean payoff: **1.076366**
- Advantage (QNE − CNE, mean): **0.731512**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.047490 | 1.807878 | yes |
| player 0 | H | 0.832528 | 1.807878 | yes |
| player 1 | D | 1.047490 | 1.807878 | yes |
| player 1 | H | 0.832528 | 1.807878 | yes |

### N=2 · w · gamma=pi/2 (V=4, C=3)

- (Q,Q) mean per-player payoff: **2.000000**
- Classical NE mean payoff: **1.250000**
- Advantage (QNE − CNE, mean): **0.750000**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.000000 | 2.000000 | yes |
| player 0 | H | 2.625000 | 2.000000 | **NO — NASH VIOLATED** |
| player 1 | D | 1.000000 | 2.000000 | yes |
| player 1 | H | 2.625000 | 2.000000 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.005 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.967299**
- Classical NE mean payoff: **1.281800**
- Advantage (QNE − CNE, mean): **0.685499**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.9671, 1.9675]
- Classical NE payoff vector: [1.2791, 1.2845]
- Advantage vector: [0.6879, 0.6831]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.055668 | 1.967068 | yes |
| player 0 | H | 2.529837 | 1.967068 | **NO — NASH VIOLATED** |
| player 1 | D | 1.061517 | 1.967530 | yes |
| player 1 | H | 2.536827 | 1.967530 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.01 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.937318**
- Classical NE mean payoff: **1.311018**
- Advantage (QNE − CNE, mean): **0.626300**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.9369, 1.9378]
- Classical NE payoff vector: [1.3061, 1.3159]
- Advantage vector: [0.6307, 0.6219]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.106532 | 1.936870 | yes |
| player 0 | H | 2.443363 | 1.936870 | **NO — NASH VIOLATED** |
| player 1 | D | 1.117222 | 1.937765 | yes |
| player 1 | H | 2.456083 | 1.937765 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.015 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.909840**
- Classical NE mean payoff: **1.337855**
- Advantage (QNE − CNE, mean): **0.571985**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.9092, 1.9105]
- Classical NE payoff vector: [1.3312, 1.3445]
- Advantage vector: [0.5780, 0.5660]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.152993 | 1.909194 | yes |
| player 0 | H | 2.364816 | 1.909194 | **NO — NASH VIOLATED** |
| player 1 | D | 1.167639 | 1.910486 | yes |
| player 1 | H | 2.382169 | 1.910486 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.02 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.884668**
- Classical NE mean payoff: **1.362497**
- Advantage (QNE − CNE, mean): **0.522171**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.8838, 1.8855]
- Classical NE payoff vector: [1.3544, 1.3706]
- Advantage vector: [0.5295, 0.5149]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.195417 | 1.883842 | yes |
| player 0 | H | 2.293502 | 1.883842 | **NO — NASH VIOLATED** |
| player 1 | D | 1.213250 | 1.885494 | yes |
| player 1 | H | 2.314536 | 1.885494 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.025 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.861616**
- Classical NE mean payoff: **1.385116**
- Advantage (QNE − CNE, mean): **0.476500**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.8606, 1.8626]
- Classical NE payoff vector: [1.3758, 1.3944]
- Advantage vector: [0.4848, 0.4682]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.234144 | 1.860630 | yes |
| player 0 | H | 2.228781 | 1.860630 | **NO — NASH VIOLATED** |
| player 1 | D | 1.254491 | 1.862602 | yes |
| player 1 | H | 2.252674 | 1.862602 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.03 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.840515**
- Classical NE mean payoff: **1.405872**
- Advantage (QNE − CNE, mean): **0.434643**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.8394, 1.8416]
- Classical NE payoff vector: [1.3957, 1.4160]
- Advantage vector: [0.4437, 0.4256]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.269484 | 1.839388 | yes |
| player 0 | H | 2.170070 | 1.839388 | **NO — NASH VIOLATED** |
| player 1 | D | 1.291765 | 1.841642 | yes |
| player 1 | H | 2.196113 | 1.841642 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.035 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.821208**
- Classical NE mean payoff: **1.424912**
- Advantage (QNE − CNE, mean): **0.396296**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.8200, 1.8225]
- Classical NE payoff vector: [1.4141, 1.4357]
- Advantage vector: [0.4058, 0.3867]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.301725 | 1.819960 | yes |
| player 0 | H | 2.116835 | 1.819960 | **NO — NASH VIOLATED** |
| player 1 | D | 1.325435 | 1.822455 | yes |
| player 1 | H | 2.144420 | 1.822455 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.04 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.803548**
- Classical NE mean payoff: **1.442371**
- Advantage (QNE − CNE, mean): **0.361178**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.8022, 1.8049]
- Classical NE payoff vector: [1.4311, 1.4536]
- Advantage vector: [0.3711, 0.3513]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.331127 | 1.802199 | yes |
| player 0 | H | 2.068587 | 1.802199 | **NO — NASH VIOLATED** |
| player 1 | D | 1.355836 | 1.804898 | yes |
| player 1 | H | 2.097196 | 1.804898 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.045 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.787404**
- Classical NE mean payoff: **1.458374**
- Advantage (QNE − CNE, mean): **0.329029**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.7860, 1.7888]
- Classical NE payoff vector: [1.4468, 1.4699]
- Advantage vector: [0.3391, 0.3189]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.357934 | 1.785971 | yes |
| player 0 | H | 2.024877 | 1.785971 | **NO — NASH VIOLATED** |
| player 1 | D | 1.383271 | 1.788837 | yes |
| player 1 | H | 2.054071 | 1.788837 | **NO — NASH VIOLATED** |

### N=2 · w · gamma=pi/2 · noise p=0.05 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q) mean per-player payoff: **1.772650**
- Classical NE mean payoff: **1.473039**
- Advantage (QNE − CNE, mean): **0.299611**
- (Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.7712, 1.7741]
- Classical NE payoff vector: [1.4614, 1.4847]
- Advantage vector: [0.3098, 0.2894]

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.382366 | 1.771151 | yes |
| player 0 | H | 1.985298 | 1.771151 | **NO — NASH VIOLATED** |
| player 1 | D | 1.408017 | 1.774149 | yes |
| player 1 | H | 2.014707 | 1.774149 | **NO — NASH VIOLATED** |

### N=2 · ring · gamma=pi/2 (V=4, C=3)

- (Q,Q) mean per-player payoff: **2.000000**
- Classical NE mean payoff: **0.500000**
- Advantage (QNE − CNE, mean): **1.500000**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.500000 | 2.000000 | yes |
| player 0 | H | 0.000000 | 2.000000 | yes |
| player 1 | D | 0.500000 | 2.000000 | yes |
| player 1 | H | 0.000000 | 2.000000 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.974586**
- Classical NE mean payoff: **0.576241**
- Advantage (QNE − CNE, mean): **1.398345**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.570971 | 1.974586 | yes |
| player 0 | H | 0.110126 | 1.974586 | yes |
| player 1 | D | 0.570971 | 1.974586 | yes |
| player 1 | H | 0.110126 | 1.974586 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.950780**
- Classical NE mean payoff: **0.647661**
- Advantage (QNE − CNE, mean): **1.303119**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.637789 | 1.950780 | yes |
| player 0 | H | 0.213288 | 1.950780 | yes |
| player 1 | D | 0.637789 | 1.950780 | yes |
| player 1 | H | 0.213288 | 1.950780 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.928486**
- Classical NE mean payoff: **0.714542**
- Advantage (QNE − CNE, mean): **1.213944**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.700678 | 1.928486 | yes |
| player 0 | H | 0.309895 | 1.928486 | yes |
| player 1 | D | 0.700678 | 1.928486 | yes |
| player 1 | H | 0.309895 | 1.928486 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.907616**
- Classical NE mean payoff: **0.777153**
- Advantage (QNE − CNE, mean): **1.130463**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.759850 | 1.907616 | yes |
| player 0 | H | 0.400332 | 1.907616 | yes |
| player 1 | D | 0.759850 | 1.907616 | yes |
| player 1 | H | 0.400332 | 1.907616 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.888085**
- Classical NE mean payoff: **0.835745**
- Advantage (QNE − CNE, mean): **1.052340**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.815508 | 1.888085 | yes |
| player 0 | H | 0.484966 | 1.888085 | yes |
| player 1 | D | 0.815508 | 1.888085 | yes |
| player 1 | H | 0.484966 | 1.888085 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.869814**
- Classical NE mean payoff: **0.890559**
- Advantage (QNE − CNE, mean): **0.979254**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.867845 | 1.869814 | yes |
| player 0 | H | 0.564141 | 1.869814 | yes |
| player 1 | D | 0.867845 | 1.869814 | yes |
| player 1 | H | 0.564141 | 1.869814 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.852727**
- Classical NE mean payoff: **0.941820**
- Advantage (QNE − CNE, mean): **0.910906**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.917042 | 1.852727 | yes |
| player 0 | H | 0.638185 | 1.852727 | yes |
| player 1 | D | 0.917042 | 1.852727 | yes |
| player 1 | H | 0.638185 | 1.852727 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.836752**
- Classical NE mean payoff: **0.989743**
- Advantage (QNE − CNE, mean): **0.847010**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.963273 | 1.836752 | yes |
| player 0 | H | 0.707406 | 1.836752 | yes |
| player 1 | D | 0.963273 | 1.836752 | yes |
| player 1 | H | 0.707406 | 1.836752 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.821824**
- Classical NE mean payoff: **1.034527**
- Advantage (QNE − CNE, mean): **0.787297**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.006704 | 1.821824 | yes |
| player 0 | H | 0.772095 | 1.821824 | yes |
| player 1 | D | 1.006704 | 1.821824 | yes |
| player 1 | H | 0.772095 | 1.821824 | yes |

### N=2 · ring · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q) mean per-player payoff: **1.807878**
- Classical NE mean payoff: **1.076366**
- Advantage (QNE − CNE, mean): **0.731512**
- (Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H)

All pure NE: (Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.047490 | 1.807878 | yes |
| player 0 | H | 0.832528 | 1.807878 | yes |
| player 1 | D | 1.047490 | 1.807878 | yes |
| player 1 | H | 0.832528 | 1.807878 | yes |

### N=3 · ghz · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.333333**
- Classical NE mean payoff: **0.333333**
- Advantage (QNE − CNE, mean): **1.000000**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.583333 | 1.333333 | yes |
| player 0 | H | 1.000000 | 1.333333 | yes |
| player 1 | D | 0.583333 | 1.333333 | yes |
| player 1 | H | 1.000000 | 1.333333 | yes |
| player 2 | D | 0.583333 | 1.333333 | yes |
| player 2 | H | 1.000000 | 1.333333 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.312297**
- Classical NE mean payoff: **0.414429**
- Advantage (QNE − CNE, mean): **0.897868**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.3103, 1.3103, 1.3162]
- Classical NE payoff vector: [0.4068, 0.4068, 0.4297]
- Advantage vector: [0.9035, 0.9035, 0.8866]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.622957 | 1.310334 | yes |
| player 0 | H | 1.039794 | 1.310334 | yes |
| player 1 | D | 0.622957 | 1.310334 | yes |
| player 1 | H | 1.039794 | 1.310334 | yes |
| player 2 | D | 0.635612 | 1.316224 | yes |
| player 2 | H | 1.040540 | 1.316224 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.293970**
- Classical NE mean payoff: **0.488181**
- Advantage (QNE − CNE, mean): **0.805789**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2903, 1.2903, 1.3014]
- Classical NE payoff vector: [0.4743, 0.4743, 0.5160]
- Advantage vector: [0.8160, 0.8160, 0.7853]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.660598 | 1.290274 | yes |
| player 0 | H | 1.074209 | 1.290274 | yes |
| player 1 | D | 0.660598 | 1.290274 | yes |
| player 1 | H | 1.074209 | 1.290274 | yes |
| player 2 | D | 0.683888 | 1.301363 | yes |
| player 2 | H | 1.075542 | 1.301363 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.278050**
- Classical NE mean payoff: **0.555238**
- Advantage (QNE − CNE, mean): **0.722812**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2728, 1.2728, 1.2885]
- Classical NE payoff vector: [0.5362, 0.5362, 0.5934]
- Advantage vector: [0.7367, 0.7367, 0.6951]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.696299 | 1.272836 | yes |
| player 0 | H | 1.103864 | 1.272836 | yes |
| player 1 | D | 0.696299 | 1.272836 | yes |
| player 1 | H | 1.103864 | 1.272836 | yes |
| player 2 | D | 0.728437 | 1.288477 | yes |
| player 2 | H | 1.105647 | 1.288477 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.264263**
- Classical NE mean payoff: **0.616193**
- Advantage (QNE − CNE, mean): **0.648070**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2577, 1.2577, 1.2773]
- Classical NE payoff vector: [0.5930, 0.5930, 0.6627]
- Advantage vector: [0.6648, 0.6648, 0.6146]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.730105 | 1.257734 | yes |
| player 0 | H | 1.129316 | 1.257734 | yes |
| player 1 | D | 0.730105 | 1.257734 | yes |
| player 1 | H | 1.129316 | 1.257734 | yes |
| player 2 | D | 0.769517 | 1.277322 | yes |
| player 2 | H | 1.131431 | 1.277322 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.252366**
- Classical NE mean payoff: **0.671590**
- Advantage (QNE − CNE, mean): **0.580776**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2447, 1.2447, 1.2677]
- Classical NE payoff vector: [0.6451, 0.6451, 0.7246]
- Advantage vector: [0.5996, 0.5996, 0.5430]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.762070 | 1.244708 | yes |
| player 0 | H | 1.151062 | 1.244708 | yes |
| player 1 | D | 0.762070 | 1.244708 | yes |
| player 1 | H | 1.151062 | 1.244708 | yes |
| player 2 | D | 0.807372 | 1.267683 | yes |
| player 2 | H | 1.153408 | 1.267683 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.242139**
- Classical NE mean payoff: **0.721922**
- Advantage (QNE − CNE, mean): **0.520217**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2335, 1.2335, 1.2594]
- Classical NE payoff vector: [0.6929, 0.6929, 0.7800]
- Advantage vector: [0.5406, 0.5406, 0.4794]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.792252 | 1.233524 | yes |
| player 0 | H | 1.169548 | 1.233524 | yes |
| player 1 | D | 0.792252 | 1.233524 | yes |
| player 1 | H | 1.169548 | 1.233524 | yes |
| player 2 | D | 0.842229 | 1.259368 | yes |
| player 2 | H | 1.172038 | 1.259368 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.233386**
- Classical NE mean payoff: **0.767644**
- Advantage (QNE − CNE, mean): **0.465742**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2240, 1.2240, 1.2522]
- Classical NE payoff vector: [0.7367, 0.7367, 0.8295]
- Advantage vector: [0.4872, 0.4872, 0.4227]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.820712 | 1.223974 | yes |
| player 0 | H | 1.185171 | 1.223974 | yes |
| player 1 | D | 0.820712 | 1.223974 | yes |
| player 1 | H | 1.185171 | 1.223974 | yes |
| player 2 | D | 0.874304 | 1.252210 | yes |
| player 2 | H | 1.187734 | 1.252210 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.225931**
- Classical NE mean payoff: **0.809166**
- Advantage (QNE − CNE, mean): **0.416765**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2159, 1.2159, 1.2461]
- Classical NE payoff vector: [0.7769, 0.7769, 0.8736]
- Advantage vector: [0.4389, 0.4389, 0.3724]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.847515 | 1.215866 | yes |
| player 0 | H | 1.198284 | 1.215866 | yes |
| player 1 | D | 0.847515 | 1.215866 | yes |
| player 1 | H | 1.198284 | 1.215866 | yes |
| player 2 | D | 0.903796 | 1.246059 | yes |
| player 2 | H | 1.200861 | 1.246059 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.219616**
- Classical NE mean payoff: **0.846866**
- Advantage (QNE − CNE, mean): **0.372750**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2090, 1.2090, 1.2408]
- Classical NE payoff vector: [0.8138, 0.8138, 0.9130]
- Advantage vector: [0.3952, 0.3952, 0.3278]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.872726 | 1.209033 | yes |
| player 0 | H | 1.209205 | 1.209033 | **NO — NASH VIOLATED** |
| player 1 | D | 0.872726 | 1.209033 | yes |
| player 1 | H | 1.209205 | 1.209033 | **NO — NASH VIOLATED** |
| player 2 | D | 0.930895 | 1.240783 | yes |
| player 2 | H | 1.211746 | 1.240783 | yes |

### N=3 · ghz · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.214302**
- Classical NE mean payoff: **0.881087**
- Advantage (QNE − CNE, mean): **0.333215**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2033, 1.2033, 1.2363]
- Classical NE payoff vector: [0.8476, 0.8476, 0.9480]
- Advantage vector: [0.3557, 0.3557, 0.2882]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.896412 | 1.203320 | yes |
| player 0 | H | 1.218214 | 1.203320 | **NO — NASH VIOLATED** |
| player 1 | D | 0.896412 | 1.203320 | yes |
| player 1 | H | 1.218214 | 1.203320 | **NO — NASH VIOLATED** |
| player 2 | D | 0.955775 | 1.236267 | yes |
| player 2 | H | 1.220680 | 1.236267 | yes |

### N=3 · w · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.333333**
- Classical NE mean payoff: **0.833333**
- Advantage (QNE − CNE, mean): **0.500000**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.888889 | 1.333333 | yes |
| player 0 | H | 2.888889 | 1.333333 | **NO — NASH VIOLATED** |
| player 1 | D | 0.888889 | 1.333333 | yes |
| player 1 | H | 2.888889 | 1.333333 | **NO — NASH VIOLATED** |
| player 2 | D | 0.888889 | 1.333333 | yes |
| player 2 | H | 2.888889 | 1.333333 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.005 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.301953**
- Classical NE mean payoff: **0.948943**
- Advantage (QNE − CNE, mean): **0.353010**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2996, 1.2945, 1.3117]
- Classical NE payoff vector: [0.9483, 0.9428, 0.9557]
- Advantage vector: [0.3513, 0.3517, 0.3561]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.038893 | 1.299607 | yes |
| player 0 | H | 2.313326 | 1.299607 | **NO — NASH VIOLATED** |
| player 1 | D | 1.032036 | 1.294511 | yes |
| player 1 | H | 2.320069 | 1.294511 | **NO — NASH VIOLATED** |
| player 2 | D | 1.006106 | 1.311741 | yes |
| player 2 | H | 2.377958 | 1.311741 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.01 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.278510**
- Classical NE mean payoff: **1.028511**
- Advantage (QNE − CNE, mean): **0.249999**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2745, 1.2678, 1.2933]
- Classical NE payoff vector: [1.0272, 1.0210, 1.0374]
- Advantage vector: [0.2473, 0.2468, 0.2558]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.123100 | 1.274482 | yes |
| player 0 | H | 1.935343 | 1.274482 | **NO — NASH VIOLATED** |
| player 1 | D | 1.114045 | 1.267796 | yes |
| player 1 | H | 1.944157 | 1.267796 | **NO — NASH VIOLATED** |
| player 2 | D | 1.082524 | 1.293252 | yes |
| player 2 | H | 2.025199 | 1.293252 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.015 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.260903**
- Classical NE mean payoff: **1.083424**
- Advantage (QNE − CNE, mean): **0.177479**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2560, 1.2494, 1.2774]
- Classical NE payoff vector: [1.0816, 1.0765, 1.0922]
- Advantage vector: [0.1743, 0.1729, 0.1852]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.169137 | 1.255951 | yes |
| player 0 | H | 1.686973 | 1.255951 | **NO — NASH VIOLATED** |
| player 1 | D | 1.160181 | 1.249376 | yes |
| player 1 | H | 1.695615 | 1.249376 | **NO — NASH VIOLATED** |
| player 2 | D | 1.131729 | 1.277382 | yes |
| player 2 | H | 1.780589 | 1.277382 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.02 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.247646**
- Classical NE mean payoff: **1.121418**
- Advantage (QNE − CNE, mean): **0.126229**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2424, 1.2367, 1.2639]
- Classical NE payoff vector: [1.1194, 1.1158, 1.1291]
- Advantage vector: [0.1230, 0.1209, 0.1348]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.193381 | 1.242402 | yes |
| player 0 | H | 1.523672 | 1.242402 | **NO — NASH VIOLATED** |
| player 1 | D | 1.185519 | 1.236659 | yes |
| player 1 | H | 1.531204 | 1.236659 | **NO — NASH VIOLATED** |
| player 2 | D | 1.162970 | 1.263879 | yes |
| player 2 | H | 1.610294 | 1.263879 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.025 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.237661**
- Classical NE mean payoff: **1.147766**
- Advantage (QNE − CNE, mean): **0.089895**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2326, 1.2279, 1.2525]
- Classical NE payoff vector: [1.1459, 1.1435, 1.1540]
- Advantage vector: [0.0867, 0.0844, 0.0986]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.205436 | 1.232570 | yes |
| player 0 | H | 1.416232 | 1.232570 | **NO — NASH VIOLATED** |
| player 1 | D | 1.198977 | 1.227871 | yes |
| player 1 | H | 1.422390 | 1.227871 | **NO — NASH VIOLATED** |
| player 2 | D | 1.182479 | 1.252542 | yes |
| player 2 | H | 1.491308 | 1.252542 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.03 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.230147**
- Classical NE mean payoff: **1.166075**
- Advantage (QNE − CNE, mean): **0.064072**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2255, 1.2218, 1.2432]
- Classical NE payoff vector: [1.1644, 1.1630, 1.1709]
- Advantage vector: [0.0611, 0.0588, 0.0723]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.210861 | 1.225483 | yes |
| player 0 | H | 1.345497 | 1.225483 | **NO — NASH VIOLATED** |
| player 1 | D | 1.205774 | 1.221796 | yes |
| player 1 | H | 1.350332 | 1.221796 | **NO — NASH VIOLATED** |
| player 2 | D | 1.194419 | 1.243163 | yes |
| player 2 | H | 1.407906 | 1.243163 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.035 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.224506**
- Classical NE mean payoff: **1.178821**
- Advantage (QNE − CNE, mean): **0.045685**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2204, 1.2176, 1.2355]
- Classical NE payoff vector: [1.1774, 1.1767, 1.1824]
- Advantage vector: [0.0430, 0.0409, 0.0531]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.212822 | 1.220407 | yes |
| player 0 | H | 1.298894 | 1.220407 | **NO — NASH VIOLATED** |
| player 1 | D | 1.208933 | 1.217597 | yes |
| player 1 | H | 1.302586 | 1.217597 | **NO — NASH VIOLATED** |
| player 2 | D | 1.201541 | 1.235515 | yes |
| player 2 | H | 1.349285 | 1.235515 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.04 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.220283**
- Classical NE mean payoff: **1.187707**
- Advantage (QNE − CNE, mean): **0.032575**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2168, 1.2147, 1.2294]
- Classical NE payoff vector: [1.1866, 1.1863, 1.1903]
- Advantage vector: [0.0302, 0.0284, 0.0391]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.213082 | 1.216791 | yes |
| player 0 | H | 1.268167 | 1.216791 | **NO — NASH VIOLATED** |
| player 1 | D | 1.210174 | 1.214696 | yes |
| player 1 | H | 1.270932 | 1.214696 | **NO — NASH VIOLATED** |
| player 2 | D | 1.205642 | 1.229361 | yes |
| player 2 | H | 1.307987 | 1.229361 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.045 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.217131**
- Classical NE mean payoff: **1.193911**
- Advantage (QNE − CNE, mean): **0.023221**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2142, 1.2127, 1.2245]
- Classical NE payoff vector: [1.1930, 1.1930, 1.1957]
- Advantage vector: [0.0212, 0.0197, 0.0287]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.212594 | 1.214230 | yes |
| player 0 | H | 1.247893 | 1.214230 | **NO — NASH VIOLATED** |
| player 1 | D | 1.210456 | 1.212694 | yes |
| player 1 | H | 1.249933 | 1.212694 | **NO — NASH VIOLATED** |
| player 2 | D | 1.207886 | 1.224470 | yes |
| player 2 | H | 1.278837 | 1.224470 | **NO — NASH VIOLATED** |

### N=3 · w · gamma=pi/2 · noise p=0.05 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q) mean per-player payoff: **1.214788**
- Classical NE mean payoff: **1.198246**
- Advantage (QNE − CNE, mean): **0.016543**
- (Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2124, 1.2113, 1.2206]
- Classical NE payoff vector: [1.1976, 1.1976, 1.1995]
- Advantage vector: [0.0148, 0.0137, 0.0211]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.211853 | 1.212425 | yes |
| player 0 | H | 1.234506 | 1.212425 | **NO — NASH VIOLATED** |
| player 1 | D | 1.210304 | 1.211315 | yes |
| player 1 | H | 1.235994 | 1.211315 | **NO — NASH VIOLATED** |
| player 2 | D | 1.209016 | 1.220625 | yes |
| player 2 | H | 1.258233 | 1.220625 | **NO — NASH VIOLATED** |

### N=3 · ring · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.333333**
- Classical NE mean payoff: **0.333333**
- Advantage (QNE − CNE, mean): **1.000000**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.833333 | 1.333333 | yes |
| player 0 | H | 0.437500 | 1.333333 | yes |
| player 1 | D | 0.833333 | 1.333333 | yes |
| player 1 | H | 0.437500 | 1.333333 | yes |
| player 2 | D | 0.833333 | 1.333333 | yes |
| player 2 | H | 0.437500 | 1.333333 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.315229**
- Classical NE mean payoff: **0.461853**
- Advantage (QNE − CNE, mean): **0.853376**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.3220, 1.3167, 1.3069]
- Classical NE payoff vector: [0.4290, 0.4587, 0.4979]
- Advantage vector: [0.8931, 0.8580, 0.8090]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.877999 | 1.322036 | yes |
| player 0 | H | 0.538202 | 1.322036 | yes |
| player 1 | D | 0.878797 | 1.316726 | yes |
| player 1 | H | 0.548911 | 1.316726 | yes |
| player 2 | D | 0.881260 | 1.306924 | yes |
| player 2 | H | 0.562797 | 1.306924 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.299708**
- Classical NE mean payoff: **0.571856**
- Advantage (QNE − CNE, mean): **0.727852**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.3114, 1.3024, 1.2853]
- Classical NE payoff vector: [0.5154, 0.5659, 0.6342]
- Advantage vector: [0.7960, 0.7365, 0.6511]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.917438 | 1.311409 | yes |
| player 0 | H | 0.626138 | 1.311409 | yes |
| player 1 | D | 0.918797 | 1.302392 | yes |
| player 1 | H | 0.644323 | 1.302392 | yes |
| player 2 | D | 0.923107 | 1.285322 | yes |
| player 2 | H | 0.668504 | 1.285322 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.286408**
- Classical NE mean payoff: **0.665956**
- Advantage (QNE − CNE, mean): **0.620451**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.3015, 1.2900, 1.2677]
- Classical NE payoff vector: [0.5934, 0.6577, 0.7468]
- Advantage vector: [0.7081, 0.6323, 0.5209]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.952255 | 1.301484 | yes |
| player 0 | H | 0.702873 | 1.301484 | yes |
| player 1 | D | 0.953988 | 1.290009 | yes |
| player 1 | H | 0.726013 | 1.290009 | yes |
| player 2 | D | 0.959643 | 1.267729 | yes |
| player 2 | H | 0.757576 | 1.267729 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.275016**
- Classical NE mean payoff: **0.746405**
- Advantage (QNE − CNE, mean): **0.528610**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2923, 1.2793, 1.2535]
- Classical NE payoff vector: [0.6635, 0.7362, 0.8395]
- Advantage vector: [0.6287, 0.5431, 0.4140]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.982985 | 1.292273 | yes |
| player 0 | H | 0.769786 | 1.292273 | yes |
| player 1 | D | 0.984948 | 1.279304 | yes |
| player 1 | H | 0.795939 | 1.279304 | yes |
| player 2 | D | 0.991539 | 1.253470 | yes |
| player 2 | H | 0.832537 | 1.253470 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.265262**
- Classical NE mean payoff: **0.815144**
- Advantage (QNE − CNE, mean): **0.450118**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2838, 1.2700, 1.2420]
- Classical NE payoff vector: [0.7265, 0.8034, 0.9156]
- Advantage vector: [0.5573, 0.4667, 0.3264]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.010101 | 1.283771 | yes |
| player 0 | H | 0.828095 | 1.283771 | yes |
| player 1 | D | 1.012185 | 1.270040 | yes |
| player 1 | H | 0.855783 | 1.270040 | yes |
| player 2 | D | 1.019381 | 1.241976 | yes |
| player 2 | H | 0.895541 | 1.241976 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.256916**
- Classical NE mean payoff: **0.873843**
- Advantage (QNE − CNE, mean): **0.383073**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2760, 1.2620, 1.2328]
- Classical NE payoff vector: [0.7828, 0.8609, 0.9779]
- Advantage vector: [0.4932, 0.4011, 0.2549]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.034023 | 1.275962 | yes |
| player 0 | H | 0.878870 | 1.275962 | yes |
| player 1 | D | 1.036144 | 1.262017 | yes |
| player 1 | H | 0.906987 | 1.262017 | yes |
| player 2 | D | 1.043682 | 1.232768 | yes |
| player 2 | H | 0.948424 | 1.232768 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.249776**
- Classical NE mean payoff: **0.923939**
- Advantage (QNE − CNE, mean): **0.325837**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2688, 1.2551, 1.2254]
- Classical NE payoff vector: [0.8331, 0.9101, 1.0286]
- Advantage vector: [0.4357, 0.3449, 0.1969]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.055120 | 1.268820 | yes |
| player 0 | H | 0.923055 | 1.268820 | yes |
| player 1 | D | 1.057218 | 1.255063 | yes |
| player 1 | H | 0.950791 | 1.255063 | yes |
| player 2 | D | 1.064891 | 1.225445 | yes |
| player 2 | H | 0.992750 | 1.225445 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.243672**
- Classical NE mean payoff: **0.966669**
- Advantage (QNE − CNE, mean): **0.277003**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2623, 1.2490, 1.2197]
- Classical NE payoff vector: [0.8779, 0.9523, 1.0698]
- Advantage vector: [0.3844, 0.2967, 0.1499]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.073721 | 1.262314 | yes |
| player 0 | H | 0.961477 | 1.262314 | yes |
| player 1 | D | 1.075752 | 1.249030 | yes |
| player 1 | H | 0.988258 | 1.249030 | yes |
| player 2 | D | 1.083398 | 1.219670 | yes |
| player 2 | H | 1.029851 | 1.219670 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.238454**
- Classical NE mean payoff: **1.003094**
- Advantage (QNE − CNE, mean): **0.235360**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2564, 1.2438, 1.2152]
- Classical NE payoff vector: [0.9178, 0.9885, 1.1030]
- Advantage vector: [0.3386, 0.2553, 0.1122]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.090116 | 1.256408 | yes |
| player 0 | H | 0.994867 | 1.256408 | yes |
| player 1 | D | 1.092049 | 1.243793 | yes |
| player 1 | H | 1.020298 | 1.243793 | yes |
| player 2 | D | 1.099544 | 1.215162 | yes |
| player 2 | H | 1.060858 | 1.215162 | yes |

### N=3 · ring · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q,Q) mean per-player payoff: **1.233997**
- Classical NE mean payoff: **1.034127**
- Advantage (QNE − CNE, mean): **0.199870**
- (Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.2511, 1.2392, 1.2117]
- Classical NE payoff vector: [0.9533, 1.0194, 1.1297]
- Advantage vector: [0.2978, 0.2198, 0.0820]

Classical pure NE in {D,H}^N: (H,H,H)

All pure NE: (Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.104561 | 1.251064 | yes |
| player 0 | H | 1.023862 | 1.251064 | yes |
| player 1 | D | 1.106378 | 1.239241 | yes |
| player 1 | H | 1.047694 | 1.239241 | yes |
| player 2 | D | 1.113630 | 1.211685 | yes |
| player 2 | H | 1.086731 | 1.211685 | yes |

### N=4 · ghz · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **1.000000**
- Classical NE mean payoff: **0.250000**
- Advantage (QNE − CNE, mean): **0.750000**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.625000 | 1.000000 | yes |
| player 0 | H | 2.000000 | 1.000000 | **NO — NASH VIOLATED** |
| player 1 | D | 0.625000 | 1.000000 | yes |
| player 1 | H | 2.000000 | 1.000000 | **NO — NASH VIOLATED** |
| player 2 | D | 0.625000 | 1.000000 | yes |
| player 2 | H | 2.000000 | 1.000000 | **NO — NASH VIOLATED** |
| player 3 | D | 0.625000 | 1.000000 | yes |
| player 3 | H | 2.000000 | 1.000000 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.981314**
- Classical NE mean payoff: **0.332747**
- Advantage (QNE − CNE, mean): **0.648568**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9826, 0.9826, 0.9740, 0.9861]
- Classical NE payoff vector: [0.3223, 0.3223, 0.3312, 0.3551]
- Advantage vector: [0.6602, 0.6602, 0.6428, 0.6310]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.650818 | 0.982564 | yes |
| player 0 | H | 1.904684 | 0.982564 | **NO — NASH VIOLATED** |
| player 1 | D | 0.650818 | 0.982564 | yes |
| player 1 | H | 1.904684 | 0.982564 | **NO — NASH VIOLATED** |
| player 2 | D | 0.650941 | 0.974018 | yes |
| player 2 | H | 1.904649 | 0.974018 | **NO — NASH VIOLATED** |
| player 3 | D | 0.663072 | 0.986110 | yes |
| player 3 | H | 1.901248 | 0.986110 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.966116**
- Classical NE mean payoff: **0.405610**
- Advantage (QNE − CNE, mean): **0.560507**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9679, 0.9679, 0.9534, 0.9753]
- Classical NE payoff vector: [0.3870, 0.3870, 0.4029, 0.4455]
- Advantage vector: [0.5809, 0.5809, 0.5505, 0.5298]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.674461 | 0.967921 | yes |
| player 0 | H | 1.817971 | 0.967921 | **NO — NASH VIOLATED** |
| player 1 | D | 0.674461 | 0.967921 | yes |
| player 1 | H | 1.817971 | 0.967921 | **NO — NASH VIOLATED** |
| player 2 | D | 0.674914 | 0.953351 | yes |
| player 2 | H | 1.817845 | 0.953351 | **NO — NASH VIOLATED** |
| player 3 | D | 0.696978 | 0.975273 | yes |
| player 3 | H | 1.811679 | 0.975273 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.953881**
- Classical NE mean payoff: **0.469779**
- Advantage (QNE − CNE, mean): **0.484101**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9557, 0.9557, 0.9371, 0.9669]
- Classical NE payoff vector: [0.4449, 0.4449, 0.4661, 0.5232]
- Advantage vector: [0.5108, 0.5108, 0.4710, 0.4437]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.696133 | 0.955719 | yes |
| player 0 | H | 1.739086 | 0.955719 | **NO — NASH VIOLATED** |
| player 1 | D | 0.696133 | 0.955719 | yes |
| player 1 | H | 1.739086 | 0.955719 | **NO — NASH VIOLATED** |
| player 2 | D | 0.697071 | 0.937146 | yes |
| player 2 | H | 1.738825 | 0.937146 | **NO — NASH VIOLATED** |
| player 3 | D | 0.727156 | 0.966940 | yes |
| player 3 | H | 1.730445 | 0.966940 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.944152**
- Classical NE mean payoff: **0.976333**
- Advantage (QNE − CNE, mean): **-0.032182**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9456, 0.9456, 0.9247, 0.9606]
- Classical NE payoff vector: [1.1309, 0.5003, 1.1246, 1.1495]
- Advantage vector: [-0.1852, 0.4453, -0.1999, -0.1889]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.716018 | 0.945647 | yes |
| player 0 | H | 1.667323 | 0.945647 | **NO — NASH VIOLATED** |
| player 1 | D | 0.716018 | 0.945647 | yes |
| player 1 | H | 1.667323 | 0.945647 | **NO — NASH VIOLATED** |
| player 2 | D | 0.717551 | 0.924669 | yes |
| player 2 | H | 1.666897 | 0.924669 | **NO — NASH VIOLATED** |
| player 3 | D | 0.753998 | 0.960645 | yes |
| player 3 | H | 1.656779 | 0.960645 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.936536**
- Classical NE mean payoff: **0.972772**
- Advantage (QNE − CNE, mean): **-0.036235**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9374, 0.9374, 0.9153, 0.9560]
- Classical NE payoff vector: [0.5840, 1.0991, 1.0901, 1.1178]
- Advantage vector: [0.3534, -0.1616, -0.1748, -0.1618]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.734277 | 0.937426 | yes |
| player 0 | H | 1.602040 | 0.937426 | **NO — NASH VIOLATED** |
| player 1 | D | 0.734277 | 0.937426 | yes |
| player 1 | H | 1.602040 | 0.937426 | **NO — NASH VIOLATED** |
| player 2 | D | 0.736482 | 0.915293 | yes |
| player 2 | H | 1.601430 | 0.915293 | **NO — NASH VIOLATED** |
| player 3 | D | 0.777858 | 0.956000 | yes |
| player 3 | H | 1.589981 | 0.956000 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.930695**
- Classical NE mean payoff: **0.969853**
- Advantage (QNE − CNE, mean): **-0.039157**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9308, 0.9308, 0.9085, 0.9527]
- Classical NE payoff vector: [1.0726, 0.6553, 1.0610, 1.0905]
- Advantage vector: [-0.1418, 0.2755, -0.1525, -0.1378]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H), (H,H,D,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.751059 | 0.930809 | yes |
| player 0 | H | 1.542655 | 0.930809 | **NO — NASH VIOLATED** |
| player 1 | D | 0.751059 | 0.930809 | yes |
| player 1 | H | 1.542655 | 0.930809 | **NO — NASH VIOLATED** |
| player 2 | D | 0.753979 | 0.908484 | yes |
| player 2 | H | 1.541850 | 0.908484 | **NO — NASH VIOLATED** |
| player 3 | D | 0.799052 | 0.952680 | yes |
| player 3 | H | 1.529420 | 0.952680 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.926337**
- Classical NE mean payoff: **0.967466**
- Advantage (QNE − CNE, mean): **-0.041129**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9256, 0.9256, 0.9038, 0.9504]
- Classical NE payoff vector: [1.0506, 0.7159, 1.0365, 1.0669]
- Advantage vector: [-0.1251, 0.2097, -0.1327, -0.1165]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H), (H,H,D,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.766496 | 0.925576 | yes |
| player 0 | H | 1.488637 | 0.925576 | **NO — NASH VIOLATED** |
| player 1 | D | 0.766496 | 0.925576 | yes |
| player 1 | H | 1.488637 | 0.925576 | **NO — NASH VIOLATED** |
| player 2 | D | 0.770150 | 0.903784 | yes |
| player 2 | H | 1.487633 | 0.903784 | **NO — NASH VIOLATED** |
| player 3 | D | 0.817863 | 0.950414 | yes |
| player 3 | H | 1.474518 | 0.950414 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.923212**
- Classical NE mean payoff: **0.965519**
- Advantage (QNE − CNE, mean): **-0.042307**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9215, 0.9215, 0.9008, 0.9490]
- Classical NE payoff vector: [0.7671, 1.0325, 1.0159, 1.0466]
- Advantage vector: [0.1544, -0.1110, -0.1150, -0.0976]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H), (H,H,D,H)

All pure NE: (H,Q,Q,D), (Q,H,Q,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.780705 | 0.921533 | yes |
| player 0 | H | 1.439504 | 0.921533 | **NO — NASH VIOLATED** |
| player 1 | D | 0.780705 | 0.921533 | yes |
| player 1 | H | 1.439504 | 0.921533 | **NO — NASH VIOLATED** |
| player 2 | D | 0.785091 | 0.900806 | yes |
| player 2 | H | 1.438303 | 0.900806 | **NO — NASH VIOLATED** |
| player 3 | D | 0.834546 | 0.948976 | yes |
| player 3 | H | 1.424755 | 0.948976 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.921105**
- Classical NE mean payoff: **0.963934**
- Advantage (QNE − CNE, mean): **-0.042829**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9185, 0.9185, 0.8992, 0.9482]
- Classical NE payoff vector: [0.8103, 1.0176, 0.9986, 1.0292]
- Advantage vector: [0.1083, -0.0991, -0.0994, -0.0810]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H), (H,H,D,H)

All pure NE: (D,H,Q,Q), (D,Q,H,Q), (H,D,Q,Q), (H,Q,D,Q), (H,Q,Q,D), (Q,D,H,Q), (Q,H,D,Q), (Q,H,Q,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.793794 | 0.918508 | yes |
| player 0 | H | 1.394817 | 0.918508 | **NO — NASH VIOLATED** |
| player 1 | D | 0.793794 | 0.918508 | yes |
| player 1 | H | 1.394817 | 0.918508 | **NO — NASH VIOLATED** |
| player 2 | D | 0.798894 | 0.899223 | yes |
| player 2 | H | 1.393425 | 0.899223 | **NO — NASH VIOLATED** |
| player 3 | D | 0.849329 | 0.948180 | yes |
| player 3 | H | 1.379655 | 0.948180 | **NO — NASH VIOLATED** |

### N=4 · ghz · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.919833**
- Classical NE mean payoff: **0.962644**
- Advantage (QNE − CNE, mean): **-0.042811**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9164, 0.9164, 0.8988, 0.9479]
- Classical NE payoff vector: [0.8465, 1.0054, 0.9843, 1.0143]
- Advantage vector: [0.0699, -0.0891, -0.0856, -0.0665]

Classical pure NE in {D,H}^N: (D,H,H,H), (H,D,H,H), (H,H,D,H)

All pure NE: (D,H,Q,Q), (D,Q,H,Q), (H,D,Q,Q), (H,Q,D,Q), (Q,D,H,Q), (Q,H,D,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.805859 | 0.916350 | yes |
| player 0 | H | 1.354176 | 0.916350 | **NO — NASH VIOLATED** |
| player 1 | D | 0.805859 | 0.916350 | yes |
| player 1 | H | 1.354176 | 0.916350 | **NO — NASH VIOLATED** |
| player 2 | D | 0.811641 | 0.898755 | yes |
| player 2 | H | 1.352603 | 0.898755 | **NO — NASH VIOLATED** |
| player 3 | D | 0.862418 | 0.947876 | yes |
| player 3 | H | 1.338788 | 0.947876 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **1.000000**
- Classical NE mean payoff: **0.625000**
- Advantage (QNE − CNE, mean): **0.375000**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.812500 | 1.000000 | yes |
| player 0 | H | 2.875000 | 1.000000 | **NO — NASH VIOLATED** |
| player 1 | D | 0.812500 | 1.000000 | yes |
| player 1 | H | 2.875000 | 1.000000 | **NO — NASH VIOLATED** |
| player 2 | D | 0.812500 | 1.000000 | yes |
| player 2 | H | 2.875000 | 1.000000 | **NO — NASH VIOLATED** |
| player 3 | D | 0.812500 | 1.000000 | yes |
| player 3 | H | 2.875000 | 1.000000 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.005 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.967165**
- Classical NE mean payoff: **0.892613**
- Advantage (QNE − CNE, mean): **0.074552**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [1.0145, 1.0041, 0.9675, 0.8825]
- Classical NE payoff vector: [0.8584, 0.8618, 0.8876, 0.9627]
- Advantage vector: [0.1561, 0.1424, 0.0799, -0.0801]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.994497 | 1.014494 | yes |
| player 0 | H | 1.276761 | 1.014494 | **NO — NASH VIOLATED** |
| player 1 | D | 0.989634 | 1.004112 | yes |
| player 1 | H | 1.274381 | 1.004112 | **NO — NASH VIOLATED** |
| player 2 | D | 0.950943 | 0.967521 | yes |
| player 2 | H | 1.289918 | 0.967521 | **NO — NASH VIOLATED** |
| player 3 | D | 0.842659 | 0.882535 | yes |
| player 3 | H | 1.384869 | 0.882535 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.01 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.957006**
- Classical NE mean payoff: **0.940498**
- Advantage (QNE − CNE, mean): **0.016508**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9778, 0.9743, 0.9598, 0.9161]
- Classical NE payoff vector: [0.9251, 0.9259, 0.9350, 0.9760]
- Advantage vector: [0.0527, 0.0484, 0.0248, -0.0599]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.975821 | 0.977806 | yes |
| player 0 | H | 1.015062 | 0.977806 | **NO — NASH VIOLATED** |
| player 1 | D | 0.973881 | 0.974272 | yes |
| player 1 | H | 1.014361 | 0.974272 | **NO — NASH VIOLATED** |
| player 2 | D | 0.958776 | 0.959829 | yes |
| player 2 | H | 1.019290 | 0.959829 | **NO — NASH VIOLATED** |
| player 3 | D | 0.906893 | 0.916117 | yes |
| player 3 | H | 1.059938 | 0.916117 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.015 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.954180**
- Classical NE mean payoff: **0.950189**
- Advantage (QNE − CNE, mean): **0.003992**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9613, 0.9604, 0.9561, 0.9389]
- Classical NE payoff vector: [0.9448, 0.9449, 0.9472, 0.9639]
- Advantage vector: [0.0166, 0.0156, 0.0089, -0.0250]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.961186 | 0.961348 | yes |
| player 0 | H | 0.966669 | 0.961348 | **NO — NASH VIOLATED** |
| player 1 | D | 0.960617 | 0.960439 | **NO — NASH VIOLATED** |
| player 1 | H | 0.966510 | 0.960439 | **NO — NASH VIOLATED** |
| player 2 | D | 0.956086 | 0.956057 | **NO — NASH VIOLATED** |
| player 2 | H | 0.967831 | 0.956057 | **NO — NASH VIOLATED** |
| player 3 | D | 0.936550 | 0.938878 | yes |
| player 3 | H | 0.981406 | 0.938878 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.02 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953414**
- Classical NE mean payoff: **0.952383**
- Advantage (QNE − CNE, mean): **0.001031**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9557, 0.9555, 0.9543, 0.9482]
- Classical NE payoff vector: [0.9506, 0.9506, 0.9511, 0.9572]
- Advantage vector: [0.0051, 0.0049, 0.0032, -0.0090]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.955693 | 0.955695 | yes |
| player 0 | H | 0.956444 | 0.955695 | **NO — NASH VIOLATED** |
| player 1 | D | 0.955542 | 0.955484 | **NO — NASH VIOLATED** |
| player 1 | H | 0.956411 | 0.955484 | **NO — NASH VIOLATED** |
| player 2 | D | 0.954305 | 0.954274 | **NO — NASH VIOLATED** |
| player 2 | H | 0.956768 | 0.954274 | **NO — NASH VIOLATED** |
| player 3 | D | 0.947568 | 0.948203 | yes |
| player 3 | H | 0.960954 | 0.948203 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.025 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953205**
- Classical NE mean payoff: **0.952927**
- Advantage (QNE − CNE, mean): **0.000279**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9539, 0.9539, 0.9535, 0.9515]
- Classical NE payoff vector: [0.9524, 0.9524, 0.9525, 0.9545]
- Advantage vector: [0.0015, 0.0015, 0.0011, -0.0030]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.953912 | 0.953908 | **NO — NASH VIOLATED** |
| player 0 | H | 0.954007 | 0.953908 | **NO — NASH VIOLATED** |
| player 1 | D | 0.953873 | 0.953860 | **NO — NASH VIOLATED** |
| player 1 | H | 0.954000 | 0.953860 | **NO — NASH VIOLATED** |
| player 2 | D | 0.953548 | 0.953539 | **NO — NASH VIOLATED** |
| player 2 | H | 0.954101 | 0.953539 | **NO — NASH VIOLATED** |
| player 3 | D | 0.951330 | 0.951514 | yes |
| player 3 | H | 0.955354 | 0.951514 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.03 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953148**
- Classical NE mean payoff: **0.953070**
- Advantage (QNE − CNE, mean): **0.000078**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9534, 0.9533, 0.9533, 0.9526]
- Classical NE payoff vector: [0.9529, 0.9529, 0.9529, 0.9536]
- Advantage vector: [0.0005, 0.0005, 0.0004, -0.0010]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.953362 | 0.953361 | **NO — NASH VIOLATED** |
| player 0 | H | 0.953372 | 0.953361 | **NO — NASH VIOLATED** |
| player 1 | D | 0.953352 | 0.953350 | **NO — NASH VIOLATED** |
| player 1 | H | 0.953370 | 0.953350 | **NO — NASH VIOLATED** |
| player 2 | D | 0.953268 | 0.953266 | **NO — NASH VIOLATED** |
| player 2 | H | 0.953399 | 0.953266 | **NO — NASH VIOLATED** |
| player 3 | D | 0.952558 | 0.952614 | yes |
| player 3 | H | 0.953771 | 0.952614 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.035 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953132**
- Classical NE mean payoff: **0.953109**
- Advantage (QNE − CNE, mean): **0.000022**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9532, 0.9532, 0.9532, 0.9530]
- Classical NE payoff vector: [0.9531, 0.9531, 0.9531, 0.9533]
- Advantage vector: [0.0001, 0.0001, 0.0001, -0.0003]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.953196 | 0.953195 | **NO — NASH VIOLATED** |
| player 0 | H | 0.953196 | 0.953195 | **NO — NASH VIOLATED** |
| player 1 | D | 0.953193 | 0.953193 | **NO — NASH VIOLATED** |
| player 1 | H | 0.953196 | 0.953193 | **NO — NASH VIOLATED** |
| player 2 | D | 0.953172 | 0.953171 | **NO — NASH VIOLATED** |
| player 2 | H | 0.953204 | 0.953171 | **NO — NASH VIOLATED** |
| player 3 | D | 0.952949 | 0.952967 | yes |
| player 3 | H | 0.953314 | 0.952967 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.04 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953127**
- Classical NE mean payoff: **0.953123**
- Advantage (QNE − CNE, mean): **0.000004**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9531, 0.9531, 0.9531, 0.9531]
- Classical NE payoff vector: [0.9531, 0.9531, 0.9531, 0.9532]
- Advantage vector: [0.0000, 0.0000, 0.0000, -0.0001]

Classical pure NE in {D,H}^N: (H,H,D,H)

All pure NE: (H,H,D,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.953146 | 0.953146 | **NO — NASH VIOLATED** |
| player 0 | H | 0.953146 | 0.953146 | yes |
| player 1 | D | 0.953145 | 0.953145 | **NO — NASH VIOLATED** |
| player 1 | H | 0.953146 | 0.953145 | **NO — NASH VIOLATED** |
| player 2 | D | 0.953140 | 0.953140 | **NO — NASH VIOLATED** |
| player 2 | H | 0.953148 | 0.953140 | **NO — NASH VIOLATED** |
| player 3 | D | 0.953071 | 0.953077 | yes |
| player 3 | H | 0.953181 | 0.953077 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.045 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953126**
- Classical NE mean payoff: **0.953124**
- Advantage (QNE − CNE, mean): **0.000001**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.9531, 0.9531, 0.9531, 0.9531]
- Classical NE payoff vector: [0.9531, 0.9531, 0.9531, 0.9531]
- Advantage vector: [0.0000, 0.0000, 0.0000, -0.0000]

Classical pure NE in {D,H}^N: (H,H,D,H)

All pure NE: (Q,H,D,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.953131 | 0.953131 | **NO — NASH VIOLATED** |
| player 0 | H | 0.953131 | 0.953131 | yes |
| player 1 | D | 0.953131 | 0.953131 | **NO — NASH VIOLATED** |
| player 1 | H | 0.953131 | 0.953131 | yes |
| player 2 | D | 0.953130 | 0.953130 | **NO — NASH VIOLATED** |
| player 2 | H | 0.953132 | 0.953130 | **NO — NASH VIOLATED** |
| player 3 | D | 0.953109 | 0.953110 | yes |
| player 3 | H | 0.953141 | 0.953110 | **NO — NASH VIOLATED** |

### N=4 · w · gamma=pi/2 · noise p=0.05 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q) mean per-player payoff: **0.953125**
- Classical NE mean payoff: **0.953125**
- Advantage (QNE − CNE, mean): **0.000000**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,H,D,H), (H,D,D,H), (H,H,D,H)

All pure NE: (H,D,D,H), (Q,H,D,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.953127 | 0.953127 | **NO — NASH VIOLATED** |
| player 0 | H | 0.953127 | 0.953127 | yes |
| player 1 | D | 0.953127 | 0.953127 | **NO — NASH VIOLATED** |
| player 1 | H | 0.953127 | 0.953127 | yes |
| player 2 | D | 0.953126 | 0.953126 | **NO — NASH VIOLATED** |
| player 2 | H | 0.953127 | 0.953126 | **NO — NASH VIOLATED** |
| player 3 | D | 0.953120 | 0.953121 | yes |
| player 3 | H | 0.953130 | 0.953121 | **NO — NASH VIOLATED** |

### N=4 · ring · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.250000**
- Classical NE mean payoff: **0.250000**
- Advantage (QNE − CNE, mean): **0.000000**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (H,H,Q,Q), (H,Q,Q,H), (Q,H,H,Q), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.125000 | 0.250000 | **NO — NASH VIOLATED** |
| player 0 | H | 0.000000 | 0.250000 | yes |
| player 1 | D | 1.125000 | 0.250000 | **NO — NASH VIOLATED** |
| player 1 | H | 0.000000 | 0.250000 | yes |
| player 2 | D | 1.125000 | 0.250000 | **NO — NASH VIOLATED** |
| player 2 | H | 0.000000 | 0.250000 | yes |
| player 3 | D | 1.125000 | 0.250000 | **NO — NASH VIOLATED** |
| player 3 | H | 0.000000 | 0.250000 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.376895**
- Classical NE mean payoff: **0.376688**
- Advantage (QNE − CNE, mean): **0.000207**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.3582, 0.3623, 0.3914, 0.3956]
- Classical NE payoff vector: [0.3458, 0.3541, 0.4034, 0.4034]
- Advantage vector: [0.0124, 0.0082, -0.0120, -0.0078]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.083642 | 0.358245 | **NO — NASH VIOLATED** |
| player 0 | H | 0.162448 | 0.358245 | yes |
| player 1 | D | 1.084873 | 0.362315 | **NO — NASH VIOLATED** |
| player 1 | H | 0.156929 | 0.362315 | yes |
| player 2 | D | 1.116891 | 0.391391 | **NO — NASH VIOLATED** |
| player 2 | H | 0.154679 | 0.391391 | yes |
| player 3 | D | 1.118290 | 0.395629 | **NO — NASH VIOLATED** |
| player 3 | H | 0.149121 | 0.395629 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.481231**
- Classical NE mean payoff: **0.480534**
- Advantage (QNE − CNE, mean): **0.000697**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.4503, 0.4570, 0.5052, 0.5124]
- Classical NE payoff vector: [0.4274, 0.4412, 0.5268, 0.5268]
- Advantage vector: [0.0230, 0.0157, -0.0215, -0.0144]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.051273 | 0.450338 | **NO — NASH VIOLATED** |
| player 0 | H | 0.297746 | 0.450338 | yes |
| player 1 | D | 1.053207 | 0.456959 | **NO — NASH VIOLATED** |
| player 1 | H | 0.288614 | 0.456959 | yes |
| player 2 | D | 1.106502 | 0.505226 | **NO — NASH VIOLATED** |
| player 2 | H | 0.284882 | 0.505226 | yes |
| player 3 | D | 1.108994 | 0.512401 | **NO — NASH VIOLATED** |
| player 3 | H | 0.275620 | 0.512401 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.566955**
- Classical NE mean payoff: **0.565637**
- Advantage (QNE − CNE, mean): **0.001318**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.5286, 0.5367, 0.5967, 0.6058]
- Classical NE payoff vector: [0.4971, 0.5143, 0.6256, 0.6256]
- Advantage vector: [0.0315, 0.0223, -0.0289, -0.0198]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.026072 | 0.528611 | **NO — NASH VIOLATED** |
| player 0 | H | 0.410341 | 0.528611 | yes |
| player 1 | D | 1.028338 | 0.536676 | **NO — NASH VIOLATED** |
| player 1 | H | 0.399018 | 0.536676 | yes |
| player 2 | D | 1.094818 | 0.596716 | **NO — NASH VIOLATED** |
| player 2 | H | 0.394379 | 0.596716 | yes |
| player 3 | D | 1.098131 | 0.605819 | **NO — NASH VIOLATED** |
| player 3 | H | 0.382812 | 0.605819 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.637337**
- Classical NE mean payoff: **0.635368**
- Advantage (QNE − CNE, mean): **0.001970**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.5951, 0.6038, 0.6701, 0.6804]
- Classical NE payoff vector: [0.5568, 0.5759, 0.7044, 0.7044]
- Advantage vector: [0.0383, 0.0279, -0.0343, -0.0240]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 1.006567 | 0.595068 | **NO — NASH VIOLATED** |
| player 0 | H | 0.503967 | 0.595068 | yes |
| player 1 | D | 1.008916 | 0.603790 | **NO — NASH VIOLATED** |
| player 1 | H | 0.491495 | 0.603790 | yes |
| player 2 | D | 1.082563 | 0.670119 | **NO — NASH VIOLATED** |
| player 2 | H | 0.486376 | 0.670119 | yes |
| player 3 | D | 1.086463 | 0.680373 | **NO — NASH VIOLATED** |
| player 3 | H | 0.473546 | 0.680373 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.695081**
- Classical NE mean payoff: **0.692495**
- Advantage (QNE − CNE, mean): **0.002586**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.6514, 0.6603, 0.7289, 0.7397]
- Classical NE payoff vector: [0.6082, 0.6280, 0.7669, 0.7669]
- Advantage vector: [0.0433, 0.0323, -0.0380, -0.0272]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.991572 | 0.651435 | **NO — NASH VIOLATED** |
| player 0 | H | 0.581754 | 0.651435 | yes |
| player 1 | D | 0.993841 | 0.660267 | **NO — NASH VIOLATED** |
| player 1 | H | 0.568886 | 0.660267 | yes |
| player 2 | D | 1.070263 | 0.728901 | **NO — NASH VIOLATED** |
| player 2 | H | 0.563598 | 0.728901 | yes |
| player 3 | D | 1.074550 | 0.739719 | **NO — NASH VIOLATED** |
| player 3 | H | 0.550264 | 0.739719 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.742420**
- Classical NE mean payoff: **0.739293**
- Advantage (QNE − CNE, mean): **0.003127**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.6992, 0.7078, 0.7759, 0.7868]
- Classical NE payoff vector: [0.6525, 0.6721, 0.8163, 0.8163]
- Advantage vector: [0.0467, 0.0356, -0.0404, -0.0295]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.980132 | 0.699194 | **NO — NASH VIOLATED** |
| player 0 | H | 0.646329 | 0.699194 | yes |
| player 1 | D | 0.982222 | 0.707769 | **NO — NASH VIOLATED** |
| player 1 | H | 0.633593 | 0.707769 | yes |
| player 2 | D | 1.058286 | 0.775884 | **NO — NASH VIOLATED** |
| player 2 | H | 0.628355 | 0.775884 | yes |
| player 3 | D | 1.062793 | 0.786831 | **NO — NASH VIOLATED** |
| player 3 | H | 0.615063 | 0.786831 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.781201**
- Classical NE mean payoff: **0.777628**
- Advantage (QNE − CNE, mean): **0.003573**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7396, 0.7477, 0.8134, 0.8241]
- Classical NE payoff vector: [0.6908, 0.7098, 0.8550, 0.8550]
- Advantage vector: [0.0488, 0.0379, -0.0416, -0.0309]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.971483 | 0.739618 | **NO — NASH VIOLATED** |
| player 0 | H | 0.699892 | 0.739618 | yes |
| player 1 | D | 0.973341 | 0.747701 | **NO — NASH VIOLATED** |
| player 1 | H | 0.687645 | 0.747701 | yes |
| player 2 | D | 1.046879 | 0.813364 | **NO — NASH VIOLATED** |
| player 2 | H | 0.682608 | 0.813364 | yes |
| player 3 | D | 1.051472 | 0.824121 | **NO — NASH VIOLATED** |
| player 3 | H | 0.669734 | 0.824121 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.812948**
- Classical NE mean payoff: **0.809031**
- Advantage (QNE − CNE, mean): **0.003917**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7738, 0.7813, 0.8432, 0.8535]
- Classical NE payoff vector: [0.7240, 0.7419, 0.8851, 0.8851]
- Advantage vector: [0.0498, 0.0393, -0.0419, -0.0315]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.965014 | 0.773797 | **NO — NASH VIOLATED** |
| player 0 | H | 0.744283 | 0.773797 | yes |
| player 1 | D | 0.966617 | 0.781250 | **NO — NASH VIOLATED** |
| player 1 | H | 0.732756 | 0.781250 | yes |
| player 2 | D | 1.036201 | 0.843200 | **NO — NASH VIOLATED** |
| player 2 | H | 0.728016 | 0.843200 | yes |
| player 3 | D | 1.040770 | 0.853545 | **NO — NASH VIOLATED** |
| player 3 | H | 0.715812 | 0.853545 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.838917**
- Classical NE mean payoff: **0.834759**
- Advantage (QNE − CNE, mean): **0.004158**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.8027, 0.8094, 0.8669, 0.8767]
- Classical NE payoff vector: [0.7529, 0.7695, 0.9083, 0.9083]
- Advantage vector: [0.0498, 0.0399, -0.0414, -0.0316]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.960237 | 0.802665 | **NO — NASH VIOLATED** |
| player 0 | H | 0.781041 | 0.802665 | yes |
| player 1 | D | 0.961584 | 0.809421 | **NO — NASH VIOLATED** |
| player 1 | H | 0.770370 | 0.809421 | yes |
| player 2 | D | 1.026340 | 0.866900 | **NO — NASH VIOLATED** |
| player 2 | H | 0.765986 | 0.866900 | yes |
| player 3 | D | 1.030802 | 0.876683 | **NO — NASH VIOLATED** |
| player 3 | H | 0.754606 | 0.876683 | yes |

### N=4 · ring · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q,Q,Q) mean per-player payoff: **0.860145**
- Classical NE mean payoff: **0.855841**
- Advantage (QNE − CNE, mean): **0.004304**
- (Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.8270, 0.8331, 0.8857, 0.8948]
- Classical NE payoff vector: [0.7780, 0.7933, 0.9260, 0.9260]
- Advantage vector: [0.0490, 0.0398, -0.0404, -0.0312]

Classical pure NE in {D,H}^N: (H,H,H,H)

All pure NE: (H,H,H,H), (Q,Q,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.956766 | 0.827022 | **NO — NASH VIOLATED** |
| player 0 | H | 0.811454 | 0.827022 | yes |
| player 1 | D | 0.957871 | 0.833061 | **NO — NASH VIOLATED** |
| player 1 | H | 0.801704 | 0.833061 | yes |
| player 2 | D | 1.017334 | 0.885684 | **NO — NASH VIOLATED** |
| player 2 | H | 0.797705 | 0.885684 | yes |
| player 3 | D | 1.021627 | 0.894811 | **NO — NASH VIOLATED** |
| player 3 | H | 0.787231 | 0.894811 | yes |

### N=5 · ghz · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.800000**
- Classical NE mean payoff: **0.200000**
- Advantage (QNE − CNE, mean): **0.600000**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.592705 | 0.800000 | yes |
| player 0 | H | 2.618034 | 0.800000 | **NO — NASH VIOLATED** |
| player 1 | D | 0.592705 | 0.800000 | yes |
| player 1 | H | 2.618034 | 0.800000 | **NO — NASH VIOLATED** |
| player 2 | D | 0.592705 | 0.800000 | yes |
| player 2 | H | 2.618034 | 0.800000 | **NO — NASH VIOLATED** |
| player 3 | D | 0.592705 | 0.800000 | yes |
| player 3 | H | 2.618034 | 0.800000 | **NO — NASH VIOLATED** |
| player 4 | D | 0.592705 | 0.800000 | yes |
| player 4 | H | 2.618034 | 0.800000 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.782889**
- Classical NE mean payoff: **0.283165**
- Advantage (QNE − CNE, mean): **0.499724**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7855, 0.7855, 0.7780, 0.7765, 0.7889]
- Classical NE payoff vector: [0.2718, 0.2718, 0.2759, 0.2861, 0.3102]
- Advantage vector: [0.5137, 0.5137, 0.5021, 0.4904, 0.4787]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (none found)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.612337 | 0.785499 | yes |
| player 0 | H | 2.381544 | 0.785499 | **NO — NASH VIOLATED** |
| player 1 | D | 0.612337 | 0.785499 | yes |
| player 1 | H | 2.381544 | 0.785499 | **NO — NASH VIOLATED** |
| player 2 | D | 0.608676 | 0.778014 | yes |
| player 2 | H | 2.384306 | 0.778014 | **NO — NASH VIOLATED** |
| player 3 | D | 0.611002 | 0.776530 | yes |
| player 3 | H | 2.384053 | 0.776530 | **NO — NASH VIOLATED** |
| player 4 | D | 0.622371 | 0.788905 | yes |
| player 4 | H | 2.378113 | 0.788905 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.769944**
- Classical NE mean payoff: **0.789418**
- Advantage (QNE − CNE, mean): **-0.019474**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7739, 0.7739, 0.7612, 0.7592, 0.7814]
- Classical NE payoff vector: [0.9003, 0.3344, 0.8937, 0.9002, 0.9185]
- Advantage vector: [-0.1264, 0.4395, -0.1325, -0.1410, -0.1371]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H)

All pure NE: (Q,Q,H,Q,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.628894 | 0.773929 | yes |
| player 0 | H | 2.177529 | 0.773929 | **NO — NASH VIOLATED** |
| player 1 | D | 0.628894 | 0.773929 | yes |
| player 1 | H | 2.177529 | 0.773929 | **NO — NASH VIOLATED** |
| player 2 | D | 0.622619 | 0.761196 | yes |
| player 2 | H | 2.182256 | 0.761196 | **NO — NASH VIOLATED** |
| player 3 | D | 0.627090 | 0.759249 | yes |
| player 3 | H | 2.181548 | 0.759249 | **NO — NASH VIOLATED** |
| player 4 | D | 0.647685 | 0.781416 | yes |
| player 4 | H | 2.171038 | 0.781416 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.760363**
- Classical NE mean payoff: **0.786037**
- Advantage (QNE − CNE, mean): **-0.025673**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7648, 0.7648, 0.7486, 0.7469, 0.7767]
- Classical NE payoff vector: [0.8481, 0.8481, 0.4495, 0.8806, 0.9038]
- Advantage vector: [-0.0833, -0.0833, 0.2991, -0.1338, -0.1271]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (D,Q,Q,H,Q), (D,Q,Q,Q,H), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,D,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,D,Q,H,Q), (Q,D,Q,Q,H), (Q,H,D,Q,Q), (Q,H,Q,D,Q), (Q,H,Q,Q,D), (Q,Q,H,Q,D), (Q,Q,Q,D,H), (Q,Q,Q,H,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.642974 | 0.764827 | yes |
| player 0 | H | 2.001306 | 0.764827 | **NO — NASH VIOLATED** |
| player 1 | D | 0.642974 | 0.764827 | yes |
| player 1 | H | 2.001306 | 0.764827 | **NO — NASH VIOLATED** |
| player 2 | D | 0.634922 | 0.748603 | yes |
| player 2 | H | 2.007367 | 0.748603 | **NO — NASH VIOLATED** |
| player 3 | D | 0.641323 | 0.746898 | yes |
| player 3 | H | 2.006097 | 0.746898 | **NO — NASH VIOLATED** |
| player 4 | D | 0.669273 | 0.776663 | yes |
| player 4 | H | 1.992154 | 0.776663 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.753486**
- Classical NE mean payoff: **0.783459**
- Advantage (QNE − CNE, mean): **-0.029973**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7578, 0.7578, 0.7394, 0.7384, 0.7740]
- Classical NE payoff vector: [0.8169, 0.8169, 0.5477, 0.8545, 0.8813]
- Advantage vector: [-0.0591, -0.0591, 0.1917, -0.1161, -0.1073]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (D,Q,Q,H,Q), (D,Q,Q,Q,H), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,D,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,D,Q,H,Q), (Q,D,Q,Q,H), (Q,H,D,Q,Q), (Q,H,Q,D,Q), (Q,H,Q,Q,D), (Q,Q,H,Q,D), (Q,Q,Q,D,H), (Q,Q,Q,H,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.655054 | 0.757792 | yes |
| player 0 | H | 1.848889 | 0.757792 | **NO — NASH VIOLATED** |
| player 1 | D | 0.655054 | 0.757792 | yes |
| player 1 | H | 1.848889 | 0.757792 | **NO — NASH VIOLATED** |
| player 2 | D | 0.645893 | 0.739448 | yes |
| player 2 | H | 1.855785 | 0.739448 | **NO — NASH VIOLATED** |
| player 3 | D | 0.653992 | 0.738447 | yes |
| player 3 | H | 1.853916 | 0.738447 | **NO — NASH VIOLATED** |
| player 4 | D | 0.687669 | 0.773951 | yes |
| player 4 | H | 1.837477 | 0.773951 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.748765**
- Classical NE mean payoff: **0.781571**
- Advantage (QNE − CNE, mean): **-0.032806**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7525, 0.7525, 0.7331, 0.7331, 0.7727]
- Classical NE payoff vector: [0.7926, 0.7926, 0.6269, 0.8334, 0.8624]
- Advantage vector: [-0.0401, -0.0401, 0.1062, -0.1004, -0.0897]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (D,Q,Q,H,Q), (D,Q,Q,Q,H), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,D,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,D,Q,H,Q), (Q,D,Q,Q,H), (Q,H,D,Q,Q), (Q,H,Q,D,Q), (Q,H,Q,Q,D), (Q,Q,H,Q,D), (Q,Q,Q,D,H), (Q,Q,Q,H,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.665518 | 0.752482 | yes |
| player 0 | H | 1.716881 | 0.752482 | **NO — NASH VIOLATED** |
| player 1 | D | 0.665518 | 0.752482 | yes |
| player 1 | H | 1.716881 | 0.752482 | **NO — NASH VIOLATED** |
| player 2 | D | 0.655773 | 0.733072 | yes |
| player 2 | H | 1.724224 | 0.733072 | **NO — NASH VIOLATED** |
| player 3 | D | 0.665331 | 0.733055 | yes |
| player 3 | H | 1.721766 | 0.733055 | **NO — NASH VIOLATED** |
| player 4 | D | 0.703330 | 0.772735 | yes |
| player 4 | H | 1.703601 | 0.772735 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.745753**
- Classical NE mean payoff: **0.780225**
- Advantage (QNE − CNE, mean): **-0.034472**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7486, 0.7486, 0.7289, 0.7300, 0.7726]
- Classical NE payoff vector: [0.7739, 0.7739, 0.6902, 0.8165, 0.8466]
- Advantage vector: [-0.0253, -0.0253, 0.0387, -0.0864, -0.0740]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H), (H,H,H,H,D)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (D,Q,Q,H,Q), (D,Q,Q,Q,H), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,D,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,D,Q,H,Q), (Q,D,Q,Q,H), (Q,H,D,Q,Q), (Q,H,Q,D,Q), (Q,H,Q,Q,D), (Q,Q,H,D,Q), (Q,Q,H,Q,D), (Q,Q,Q,D,H), (Q,Q,Q,H,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.674669 | 0.748604 | yes |
| player 0 | H | 1.602386 | 0.748604 | **NO — NASH VIOLATED** |
| player 1 | D | 0.674669 | 0.748604 | yes |
| player 1 | H | 1.602386 | 0.748604 | **NO — NASH VIOLATED** |
| player 2 | D | 0.664751 | 0.728930 | yes |
| player 2 | H | 1.609879 | 0.728930 | **NO — NASH VIOLATED** |
| player 3 | D | 0.675532 | 0.730039 | yes |
| player 3 | H | 1.606874 | 0.730039 | **NO — NASH VIOLATED** |
| player 4 | D | 0.716650 | 0.772586 | yes |
| player 4 | H | 1.587608 | 0.772586 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.744080**
- Classical NE mean payoff: **0.779298**
- Advantage (QNE − CNE, mean): **-0.035218**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7459, 0.7459, 0.7266, 0.7288, 0.7732]
- Classical NE payoff vector: [0.7598, 0.7598, 0.7404, 0.8030, 0.8334]
- Advantage vector: [-0.0139, -0.0139, -0.0138, -0.0742, -0.0602]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H), (H,H,H,H,D)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (D,Q,Q,H,Q), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,D,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,D,Q,H,Q), (Q,H,D,Q,Q), (Q,H,Q,D,Q), (Q,H,Q,Q,D), (Q,Q,H,D,Q), (Q,Q,H,Q,D), (Q,Q,Q,D,H), (Q,Q,Q,H,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.682749 | 0.745908 | yes |
| player 0 | H | 1.502937 | 0.745908 | **NO — NASH VIOLATED** |
| player 1 | D | 0.682749 | 0.745908 | yes |
| player 1 | H | 1.502937 | 0.745908 | **NO — NASH VIOLATED** |
| player 2 | D | 0.672974 | 0.726567 | yes |
| player 2 | H | 1.510352 | 0.726567 | **NO — NASH VIOLATED** |
| player 3 | D | 0.684751 | 0.728843 | yes |
| player 3 | H | 1.506862 | 0.728843 | **NO — NASH VIOLATED** |
| player 4 | D | 0.727964 | 0.773173 | yes |
| player 4 | H | 1.487001 | 0.773173 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.743446**
- Classical NE mean payoff: **0.778694**
- Advantage (QNE − CNE, mean): **-0.035248**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7442, 0.7442, 0.7256, 0.7290, 0.7742]
- Classical NE payoff vector: [0.7495, 0.7495, 0.7797, 0.7925, 0.8224]
- Advantage vector: [-0.0053, -0.0053, -0.0541, -0.0634, -0.0482]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H), (H,H,H,H,D)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (D,Q,Q,H,Q), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,D,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,D,Q,H,Q), (Q,H,D,Q,Q), (Q,H,Q,D,Q), (Q,H,Q,Q,D), (Q,Q,H,D,Q), (Q,Q,H,Q,D), (Q,Q,Q,H,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.689951 | 0.744180 | yes |
| player 0 | H | 1.416428 | 0.744180 | **NO — NASH VIOLATED** |
| player 1 | D | 0.689951 | 0.744180 | yes |
| player 1 | H | 1.416428 | 0.744180 | **NO — NASH VIOLATED** |
| player 2 | D | 0.680557 | 0.725608 | yes |
| player 2 | H | 1.423597 | 0.725608 | **NO — NASH VIOLATED** |
| player 3 | D | 0.693116 | 0.729022 | yes |
| player 3 | H | 1.419696 | 0.729022 | **NO — NASH VIOLATED** |
| player 4 | D | 0.737562 | 0.774240 | yes |
| player 4 | H | 1.399643 | 0.774240 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.743607**
- Classical NE mean payoff: **0.778334**
- Advantage (QNE − CNE, mean): **-0.034727**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7432, 0.7432, 0.7257, 0.7302, 0.7756]
- Classical NE payoff vector: [0.7421, 0.7421, 0.8100, 0.7843, 0.8133]
- Advantage vector: [0.0012, 0.0012, -0.0842, -0.0541, -0.0377]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H), (H,H,H,H,D)

All pure NE: (D,H,Q,Q,Q), (D,Q,H,Q,Q), (H,D,Q,Q,Q), (H,Q,D,Q,Q), (H,Q,Q,H,Q), (H,Q,Q,Q,D), (Q,D,H,Q,Q), (Q,H,D,Q,Q), (Q,H,Q,H,Q), (Q,H,Q,Q,D), (Q,Q,H,D,Q), (Q,Q,H,Q,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.696427 | 0.743242 | yes |
| player 0 | H | 1.341060 | 0.743242 | **NO — NASH VIOLATED** |
| player 1 | D | 0.696427 | 0.743242 | yes |
| player 1 | H | 1.341060 | 0.743242 | **NO — NASH VIOLATED** |
| player 2 | D | 0.687589 | 0.725742 | yes |
| player 2 | H | 1.347864 | 0.725742 | **NO — NASH VIOLATED** |
| player 3 | D | 0.700732 | 0.730216 | yes |
| player 3 | H | 1.343628 | 0.730216 | **NO — NASH VIOLATED** |
| player 4 | D | 0.745690 | 0.775595 | yes |
| player 4 | H | 1.323702 | 0.775595 | **NO — NASH VIOLATED** |

### N=5 · ghz · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.744364**
- Classical NE mean payoff: **0.778158**
- Advantage (QNE − CNE, mean): **-0.033793**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7429, 0.7429, 0.7267, 0.7321, 0.7771]
- Classical NE payoff vector: [0.7371, 0.7371, 0.8329, 0.7780, 0.8057]
- Advantage vector: [0.0058, 0.0058, -0.1062, -0.0459, -0.0286]

Classical pure NE in {D,H}^N: (D,H,H,H,H), (H,D,H,H,H), (H,H,D,H,H), (H,H,H,D,H)

All pure NE: (D,H,Q,Q,Q), (H,D,Q,Q,Q), (H,Q,H,Q,Q), (H,Q,Q,H,Q), (Q,H,H,Q,Q), (Q,H,Q,H,Q), (Q,Q,H,D,Q), (Q,Q,H,Q,D)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.702297 | 0.742939 | yes |
| player 0 | H | 1.275298 | 0.742939 | **NO — NASH VIOLATED** |
| player 1 | D | 0.702297 | 0.742939 | yes |
| player 1 | H | 1.275298 | 0.742939 | **NO — NASH VIOLATED** |
| player 2 | D | 0.694140 | 0.726714 | yes |
| player 2 | H | 1.281654 | 0.726714 | **NO — NASH VIOLATED** |
| player 3 | D | 0.707685 | 0.732140 | yes |
| player 3 | H | 1.277161 | 0.732140 | **NO — NASH VIOLATED** |
| player 4 | D | 0.752561 | 0.777092 | yes |
| player 4 | H | 1.257610 | 0.777092 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.800000**
- Classical NE mean payoff: **0.500000**
- Advantage (QNE − CNE, mean): **0.300000**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.711554 | 0.800000 | yes |
| player 0 | H | 2.880000 | 0.800000 | **NO — NASH VIOLATED** |
| player 1 | D | 0.711554 | 0.800000 | yes |
| player 1 | H | 2.880000 | 0.800000 | **NO — NASH VIOLATED** |
| player 2 | D | 0.711554 | 0.800000 | yes |
| player 2 | H | 2.880000 | 0.800000 | **NO — NASH VIOLATED** |
| player 3 | D | 0.711554 | 0.800000 | yes |
| player 3 | H | 2.880000 | 0.800000 | **NO — NASH VIOLATED** |
| player 4 | D | 0.711554 | 0.800000 | yes |
| player 4 | H | 2.880000 | 0.800000 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 · noise p=0.005 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781498**
- Classical NE mean payoff: **0.780315**
- Advantage (QNE − CNE, mean): **0.001183**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7871, 0.7873, 0.7867, 0.7825, 0.7638]
- Classical NE payoff vector: [0.7763, 0.7764, 0.7764, 0.7774, 0.7951]
- Advantage vector: [0.0109, 0.0109, 0.0103, 0.0051, -0.0312]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.787156 | 0.787127 | **NO — NASH VIOLATED** |
| player 0 | H | 0.787448 | 0.787127 | **NO — NASH VIOLATED** |
| player 1 | D | 0.787350 | 0.787336 | **NO — NASH VIOLATED** |
| player 1 | H | 0.787565 | 0.787336 | **NO — NASH VIOLATED** |
| player 2 | D | 0.786732 | 0.786702 | **NO — NASH VIOLATED** |
| player 2 | H | 0.787132 | 0.786702 | **NO — NASH VIOLATED** |
| player 3 | D | 0.782483 | 0.782491 | yes |
| player 3 | H | 0.789363 | 0.782491 | **NO — NASH VIOLATED** |
| player 4 | D | 0.763528 | 0.763833 | yes |
| player 4 | H | 0.801511 | 0.763833 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 · noise p=0.01 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781255**
- Classical NE mean payoff: **0.781244**
- Advantage (QNE − CNE, mean): **0.000011**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7814, 0.7814, 0.7814, 0.7813, 0.7808]
- Classical NE payoff vector: [0.7811, 0.7811, 0.7811, 0.7811, 0.7817]
- Advantage vector: [0.0003, 0.0003, 0.0003, 0.0002, -0.0010]

Classical pure NE in {D,H}^N: (D,D,H,D,H), (D,H,D,D,H)

All pure NE: (D,D,H,D,H), (D,H,D,D,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781396 | 0.781395 | **NO — NASH VIOLATED** |
| player 0 | H | 0.781393 | 0.781395 | yes |
| player 1 | D | 0.781401 | 0.781400 | **NO — NASH VIOLATED** |
| player 1 | H | 0.781396 | 0.781400 | yes |
| player 2 | D | 0.781391 | 0.781391 | **NO — NASH VIOLATED** |
| player 2 | H | 0.781389 | 0.781391 | yes |
| player 3 | D | 0.781330 | 0.781331 | yes |
| player 3 | H | 0.781437 | 0.781331 | **NO — NASH VIOLATED** |
| player 4 | D | 0.780750 | 0.780757 | yes |
| player 4 | H | 0.781754 | 0.780757 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 · noise p=0.015 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7813, 0.7813, 0.7813, 0.7813, 0.7812]
- Classical NE payoff vector: [0.7812, 0.7812, 0.7812, 0.7812, 0.7813]
- Advantage vector: [0.0000, 0.0000, 0.0000, 0.0000, -0.0000]

Classical pure NE in {D,H}^N: (D,D,H,D,H), (D,H,D,D,H)

All pure NE: (D,D,H,D,H), (D,H,D,D,H), (D,H,Q,D,H), (Q,H,H,D,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781254 | 0.781254 | **NO — NASH VIOLATED** |
| player 0 | H | 0.781254 | 0.781254 | yes |
| player 1 | D | 0.781254 | 0.781254 | **NO — NASH VIOLATED** |
| player 1 | H | 0.781254 | 0.781254 | yes |
| player 2 | D | 0.781254 | 0.781254 | **NO — NASH VIOLATED** |
| player 2 | H | 0.781254 | 0.781254 | yes |
| player 3 | D | 0.781252 | 0.781252 | yes |
| player 3 | H | 0.781255 | 0.781252 | **NO — NASH VIOLATED** |
| player 4 | D | 0.781236 | 0.781236 | yes |
| player 4 | H | 0.781264 | 0.781236 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 · noise p=0.02 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,H,D,H), (D,H,D,D,H), (D,H,H,D,H), (H,D,D,D,H), (H,D,H,D,H), (H,H,D,D,H), (H,H,H,D,H)

All pure NE: (D,D,H,D,H), (D,H,D,D,H), (D,H,H,D,H), (D,H,Q,D,H), (D,Q,H,D,H), (H,D,D,D,H), (H,D,H,D,H), (H,D,Q,D,H), (H,H,D,D,H), (H,H,H,D,H), (H,H,Q,D,H), (H,Q,D,D,H), (H,Q,H,D,H), (H,Q,Q,D,H), (Q,D,H,D,H), (Q,H,D,D,H), (Q,H,H,D,H), (Q,H,Q,D,H), (Q,Q,H,D,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | **NO — NASH VIOLATED** |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 · noise p=0.025 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,D,D,H), (D,D,H,D,H), (D,H,D,D,H), (D,H,H,D,H), (H,D,D,D,H), (H,D,H,D,H), (H,H,D,D,H), (H,H,H,D,H)

All pure NE: (D,D,D,D,H), (D,D,D,Q,H), (D,D,H,D,H), (D,D,H,Q,H), (D,D,Q,D,H), (D,D,Q,Q,H), (D,H,D,D,H), (D,H,D,Q,H), (D,H,H,D,H), (D,H,H,Q,H), (D,H,Q,D,H), (D,H,Q,Q,H), (D,Q,D,D,H), (D,Q,D,Q,H), (D,Q,H,D,H), (D,Q,H,Q,H), (D,Q,Q,D,H), (D,Q,Q,Q,H), (H,D,D,D,H), (H,D,D,Q,H), (H,D,H,D,H), (H,D,H,Q,H), (H,D,Q,D,H), (H,D,Q,Q,H), (H,H,D,D,H), (H,H,D,Q,H), (H,H,H,D,H), (H,H,H,Q,H), (H,H,Q,D,H), (H,H,Q,Q,H), (H,Q,D,D,H), (H,Q,D,Q,H), (H,Q,H,D,H), (H,Q,H,Q,H), (H,Q,Q,D,H), (H,Q,Q,Q,H), (Q,D,D,D,H), (Q,D,D,Q,H), (Q,D,H,D,H), (Q,D,H,Q,H), (Q,D,Q,D,H), (Q,D,Q,Q,H), (Q,H,D,D,H), (Q,H,D,Q,H), (Q,H,H,D,H), (Q,H,H,Q,H), (Q,H,Q,D,H), (Q,H,Q,Q,H), (Q,Q,D,D,H), (Q,Q,D,Q,H), (Q,Q,H,D,H), (Q,Q,H,Q,H), (Q,Q,Q,D,H), (Q,Q,Q,Q,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | **NO — NASH VIOLATED** |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | **NO — NASH VIOLATED** |

### N=5 · w · gamma=pi/2 · noise p=0.03 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **-0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,H,D), (D,D,D,H,H), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,H,D), (D,D,H,H,H), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,H,D), (D,H,D,H,H), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,H,D), (D,H,H,H,H), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,H,D), (H,D,D,H,H), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,H,D), (H,D,H,H,H), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,H,D), (H,H,D,H,H), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,H,D), (H,H,H,H,H)

All pure NE: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,D,Q), (D,D,D,H,D), (D,D,D,H,H), (D,D,D,H,Q), (D,D,D,Q,D), (D,D,D,Q,H), (D,D,D,Q,Q), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,D,Q), (D,D,H,H,D), (D,D,H,H,H), (D,D,H,H,Q), (D,D,H,Q,D), (D,D,H,Q,H), (D,D,H,Q,Q), (D,D,Q,D,D), (D,D,Q,D,H), (D,D,Q,D,Q), (D,D,Q,H,D), (D,D,Q,H,H), (D,D,Q,H,Q), (D,D,Q,Q,D), (D,D,Q,Q,H), (D,D,Q,Q,Q), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,D,Q), (D,H,D,H,D), (D,H,D,H,H), (D,H,D,H,Q), (D,H,D,Q,D), (D,H,D,Q,H), (D,H,D,Q,Q), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,D,Q), (D,H,H,H,D), (D,H,H,H,H), (D,H,H,H,Q), (D,H,H,Q,D), (D,H,H,Q,H), (D,H,H,Q,Q), (D,H,Q,D,D), (D,H,Q,D,H), (D,H,Q,D,Q), (D,H,Q,H,D), (D,H,Q,H,H), (D,H,Q,H,Q), (D,H,Q,Q,D), (D,H,Q,Q,H), (D,H,Q,Q,Q), (D,Q,D,D,D), (D,Q,D,D,H), (D,Q,D,D,Q), (D,Q,D,H,D), (D,Q,D,H,H), (D,Q,D,H,Q), (D,Q,D,Q,D), (D,Q,D,Q,H), (D,Q,D,Q,Q), (D,Q,H,D,D), (D,Q,H,D,H), (D,Q,H,D,Q), (D,Q,H,H,D), (D,Q,H,H,H), (D,Q,H,H,Q), (D,Q,H,Q,D), (D,Q,H,Q,H), (D,Q,H,Q,Q), (D,Q,Q,D,D), (D,Q,Q,D,H), (D,Q,Q,D,Q), (D,Q,Q,H,D), (D,Q,Q,H,H), (D,Q,Q,H,Q), (D,Q,Q,Q,D), (D,Q,Q,Q,H), (D,Q,Q,Q,Q), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,D,Q), (H,D,D,H,D), (H,D,D,H,H), (H,D,D,H,Q), (H,D,D,Q,D), (H,D,D,Q,H), (H,D,D,Q,Q), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,D,Q), (H,D,H,H,D), (H,D,H,H,H), (H,D,H,H,Q), (H,D,H,Q,D), (H,D,H,Q,H), (H,D,H,Q,Q), (H,D,Q,D,D), (H,D,Q,D,H), (H,D,Q,D,Q), (H,D,Q,H,D), (H,D,Q,H,H), (H,D,Q,H,Q), (H,D,Q,Q,D), (H,D,Q,Q,H), (H,D,Q,Q,Q), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,D,Q), (H,H,D,H,D), (H,H,D,H,H), (H,H,D,H,Q), (H,H,D,Q,D), (H,H,D,Q,H), (H,H,D,Q,Q), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,D,Q), (H,H,H,H,D), (H,H,H,H,H), (H,H,H,H,Q), (H,H,H,Q,D), (H,H,H,Q,H), (H,H,H,Q,Q), (H,H,Q,D,D), (H,H,Q,D,H), (H,H,Q,D,Q), (H,H,Q,H,D), (H,H,Q,H,H), (H,H,Q,H,Q), (H,H,Q,Q,D), (H,H,Q,Q,H), (H,H,Q,Q,Q), (H,Q,D,D,D), (H,Q,D,D,H), (H,Q,D,D,Q), (H,Q,D,H,D), (H,Q,D,H,H), (H,Q,D,H,Q), (H,Q,D,Q,D), (H,Q,D,Q,H), (H,Q,D,Q,Q), (H,Q,H,D,D), (H,Q,H,D,H), (H,Q,H,D,Q), (H,Q,H,H,D), (H,Q,H,H,H), (H,Q,H,H,Q), (H,Q,H,Q,D), (H,Q,H,Q,H), (H,Q,H,Q,Q), (H,Q,Q,D,D), (H,Q,Q,D,H), (H,Q,Q,D,Q), (H,Q,Q,H,D), (H,Q,Q,H,H), (H,Q,Q,H,Q), (H,Q,Q,Q,D), (H,Q,Q,Q,H), (H,Q,Q,Q,Q), (Q,D,D,D,D), (Q,D,D,D,H), (Q,D,D,D,Q), (Q,D,D,H,D), (Q,D,D,H,H), (Q,D,D,H,Q), (Q,D,D,Q,D), (Q,D,D,Q,H), (Q,D,D,Q,Q), (Q,D,H,D,D), (Q,D,H,D,H), (Q,D,H,D,Q), (Q,D,H,H,D), (Q,D,H,H,H), (Q,D,H,H,Q), (Q,D,H,Q,D), (Q,D,H,Q,H), (Q,D,H,Q,Q), (Q,D,Q,D,D), (Q,D,Q,D,H), (Q,D,Q,D,Q), (Q,D,Q,H,D), (Q,D,Q,H,H), (Q,D,Q,H,Q), (Q,D,Q,Q,D), (Q,D,Q,Q,H), (Q,D,Q,Q,Q), (Q,H,D,D,D), (Q,H,D,D,H), (Q,H,D,D,Q), (Q,H,D,H,D), (Q,H,D,H,H), (Q,H,D,H,Q), (Q,H,D,Q,D), (Q,H,D,Q,H), (Q,H,D,Q,Q), (Q,H,H,D,D), (Q,H,H,D,H), (Q,H,H,D,Q), (Q,H,H,H,D), (Q,H,H,H,H), (Q,H,H,H,Q), (Q,H,H,Q,D), (Q,H,H,Q,H), (Q,H,H,Q,Q), (Q,H,Q,D,D), (Q,H,Q,D,H), (Q,H,Q,D,Q), (Q,H,Q,H,D), (Q,H,Q,H,H), (Q,H,Q,H,Q), (Q,H,Q,Q,D), (Q,H,Q,Q,H), (Q,H,Q,Q,Q), (Q,Q,D,D,D), (Q,Q,D,D,H), (Q,Q,D,D,Q), (Q,Q,D,H,D), (Q,Q,D,H,H), (Q,Q,D,H,Q), (Q,Q,D,Q,D), (Q,Q,D,Q,H), (Q,Q,D,Q,Q), (Q,Q,H,D,D), (Q,Q,H,D,H), (Q,Q,H,D,Q), (Q,Q,H,H,D), (Q,Q,H,H,H), (Q,Q,H,H,Q), (Q,Q,H,Q,D), (Q,Q,H,Q,H), (Q,Q,H,Q,Q), (Q,Q,Q,D,D), (Q,Q,Q,D,H), (Q,Q,Q,D,Q), (Q,Q,Q,H,D), (Q,Q,Q,H,H), (Q,Q,Q,H,Q), (Q,Q,Q,Q,D), (Q,Q,Q,Q,H), (Q,Q,Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | yes |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | yes |

### N=5 · w · gamma=pi/2 · noise p=0.035 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **-0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,H,D), (D,D,D,H,H), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,H,D), (D,D,H,H,H), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,H,D), (D,H,D,H,H), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,H,D), (D,H,H,H,H), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,H,D), (H,D,D,H,H), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,H,D), (H,D,H,H,H), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,H,D), (H,H,D,H,H), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,H,D), (H,H,H,H,H)

All pure NE: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,D,Q), (D,D,D,H,D), (D,D,D,H,H), (D,D,D,H,Q), (D,D,D,Q,D), (D,D,D,Q,H), (D,D,D,Q,Q), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,D,Q), (D,D,H,H,D), (D,D,H,H,H), (D,D,H,H,Q), (D,D,H,Q,D), (D,D,H,Q,H), (D,D,H,Q,Q), (D,D,Q,D,D), (D,D,Q,D,H), (D,D,Q,D,Q), (D,D,Q,H,D), (D,D,Q,H,H), (D,D,Q,H,Q), (D,D,Q,Q,D), (D,D,Q,Q,H), (D,D,Q,Q,Q), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,D,Q), (D,H,D,H,D), (D,H,D,H,H), (D,H,D,H,Q), (D,H,D,Q,D), (D,H,D,Q,H), (D,H,D,Q,Q), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,D,Q), (D,H,H,H,D), (D,H,H,H,H), (D,H,H,H,Q), (D,H,H,Q,D), (D,H,H,Q,H), (D,H,H,Q,Q), (D,H,Q,D,D), (D,H,Q,D,H), (D,H,Q,D,Q), (D,H,Q,H,D), (D,H,Q,H,H), (D,H,Q,H,Q), (D,H,Q,Q,D), (D,H,Q,Q,H), (D,H,Q,Q,Q), (D,Q,D,D,D), (D,Q,D,D,H), (D,Q,D,D,Q), (D,Q,D,H,D), (D,Q,D,H,H), (D,Q,D,H,Q), (D,Q,D,Q,D), (D,Q,D,Q,H), (D,Q,D,Q,Q), (D,Q,H,D,D), (D,Q,H,D,H), (D,Q,H,D,Q), (D,Q,H,H,D), (D,Q,H,H,H), (D,Q,H,H,Q), (D,Q,H,Q,D), (D,Q,H,Q,H), (D,Q,H,Q,Q), (D,Q,Q,D,D), (D,Q,Q,D,H), (D,Q,Q,D,Q), (D,Q,Q,H,D), (D,Q,Q,H,H), (D,Q,Q,H,Q), (D,Q,Q,Q,D), (D,Q,Q,Q,H), (D,Q,Q,Q,Q), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,D,Q), (H,D,D,H,D), (H,D,D,H,H), (H,D,D,H,Q), (H,D,D,Q,D), (H,D,D,Q,H), (H,D,D,Q,Q), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,D,Q), (H,D,H,H,D), (H,D,H,H,H), (H,D,H,H,Q), (H,D,H,Q,D), (H,D,H,Q,H), (H,D,H,Q,Q), (H,D,Q,D,D), (H,D,Q,D,H), (H,D,Q,D,Q), (H,D,Q,H,D), (H,D,Q,H,H), (H,D,Q,H,Q), (H,D,Q,Q,D), (H,D,Q,Q,H), (H,D,Q,Q,Q), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,D,Q), (H,H,D,H,D), (H,H,D,H,H), (H,H,D,H,Q), (H,H,D,Q,D), (H,H,D,Q,H), (H,H,D,Q,Q), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,D,Q), (H,H,H,H,D), (H,H,H,H,H), (H,H,H,H,Q), (H,H,H,Q,D), (H,H,H,Q,H), (H,H,H,Q,Q), (H,H,Q,D,D), (H,H,Q,D,H), (H,H,Q,D,Q), (H,H,Q,H,D), (H,H,Q,H,H), (H,H,Q,H,Q), (H,H,Q,Q,D), (H,H,Q,Q,H), (H,H,Q,Q,Q), (H,Q,D,D,D), (H,Q,D,D,H), (H,Q,D,D,Q), (H,Q,D,H,D), (H,Q,D,H,H), (H,Q,D,H,Q), (H,Q,D,Q,D), (H,Q,D,Q,H), (H,Q,D,Q,Q), (H,Q,H,D,D), (H,Q,H,D,H), (H,Q,H,D,Q), (H,Q,H,H,D), (H,Q,H,H,H), (H,Q,H,H,Q), (H,Q,H,Q,D), (H,Q,H,Q,H), (H,Q,H,Q,Q), (H,Q,Q,D,D), (H,Q,Q,D,H), (H,Q,Q,D,Q), (H,Q,Q,H,D), (H,Q,Q,H,H), (H,Q,Q,H,Q), (H,Q,Q,Q,D), (H,Q,Q,Q,H), (H,Q,Q,Q,Q), (Q,D,D,D,D), (Q,D,D,D,H), (Q,D,D,D,Q), (Q,D,D,H,D), (Q,D,D,H,H), (Q,D,D,H,Q), (Q,D,D,Q,D), (Q,D,D,Q,H), (Q,D,D,Q,Q), (Q,D,H,D,D), (Q,D,H,D,H), (Q,D,H,D,Q), (Q,D,H,H,D), (Q,D,H,H,H), (Q,D,H,H,Q), (Q,D,H,Q,D), (Q,D,H,Q,H), (Q,D,H,Q,Q), (Q,D,Q,D,D), (Q,D,Q,D,H), (Q,D,Q,D,Q), (Q,D,Q,H,D), (Q,D,Q,H,H), (Q,D,Q,H,Q), (Q,D,Q,Q,D), (Q,D,Q,Q,H), (Q,D,Q,Q,Q), (Q,H,D,D,D), (Q,H,D,D,H), (Q,H,D,D,Q), (Q,H,D,H,D), (Q,H,D,H,H), (Q,H,D,H,Q), (Q,H,D,Q,D), (Q,H,D,Q,H), (Q,H,D,Q,Q), (Q,H,H,D,D), (Q,H,H,D,H), (Q,H,H,D,Q), (Q,H,H,H,D), (Q,H,H,H,H), (Q,H,H,H,Q), (Q,H,H,Q,D), (Q,H,H,Q,H), (Q,H,H,Q,Q), (Q,H,Q,D,D), (Q,H,Q,D,H), (Q,H,Q,D,Q), (Q,H,Q,H,D), (Q,H,Q,H,H), (Q,H,Q,H,Q), (Q,H,Q,Q,D), (Q,H,Q,Q,H), (Q,H,Q,Q,Q), (Q,Q,D,D,D), (Q,Q,D,D,H), (Q,Q,D,D,Q), (Q,Q,D,H,D), (Q,Q,D,H,H), (Q,Q,D,H,Q), (Q,Q,D,Q,D), (Q,Q,D,Q,H), (Q,Q,D,Q,Q), (Q,Q,H,D,D), (Q,Q,H,D,H), (Q,Q,H,D,Q), (Q,Q,H,H,D), (Q,Q,H,H,H), (Q,Q,H,H,Q), (Q,Q,H,Q,D), (Q,Q,H,Q,H), (Q,Q,H,Q,Q), (Q,Q,Q,D,D), (Q,Q,Q,D,H), (Q,Q,Q,D,Q), (Q,Q,Q,H,D), (Q,Q,Q,H,H), (Q,Q,Q,H,Q), (Q,Q,Q,Q,D), (Q,Q,Q,Q,H), (Q,Q,Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | yes |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | yes |

### N=5 · w · gamma=pi/2 · noise p=0.04 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **-0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,H,D), (D,D,D,H,H), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,H,D), (D,D,H,H,H), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,H,D), (D,H,D,H,H), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,H,D), (D,H,H,H,H), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,H,D), (H,D,D,H,H), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,H,D), (H,D,H,H,H), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,H,D), (H,H,D,H,H), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,H,D), (H,H,H,H,H)

All pure NE: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,D,Q), (D,D,D,H,D), (D,D,D,H,H), (D,D,D,H,Q), (D,D,D,Q,D), (D,D,D,Q,H), (D,D,D,Q,Q), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,D,Q), (D,D,H,H,D), (D,D,H,H,H), (D,D,H,H,Q), (D,D,H,Q,D), (D,D,H,Q,H), (D,D,H,Q,Q), (D,D,Q,D,D), (D,D,Q,D,H), (D,D,Q,D,Q), (D,D,Q,H,D), (D,D,Q,H,H), (D,D,Q,H,Q), (D,D,Q,Q,D), (D,D,Q,Q,H), (D,D,Q,Q,Q), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,D,Q), (D,H,D,H,D), (D,H,D,H,H), (D,H,D,H,Q), (D,H,D,Q,D), (D,H,D,Q,H), (D,H,D,Q,Q), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,D,Q), (D,H,H,H,D), (D,H,H,H,H), (D,H,H,H,Q), (D,H,H,Q,D), (D,H,H,Q,H), (D,H,H,Q,Q), (D,H,Q,D,D), (D,H,Q,D,H), (D,H,Q,D,Q), (D,H,Q,H,D), (D,H,Q,H,H), (D,H,Q,H,Q), (D,H,Q,Q,D), (D,H,Q,Q,H), (D,H,Q,Q,Q), (D,Q,D,D,D), (D,Q,D,D,H), (D,Q,D,D,Q), (D,Q,D,H,D), (D,Q,D,H,H), (D,Q,D,H,Q), (D,Q,D,Q,D), (D,Q,D,Q,H), (D,Q,D,Q,Q), (D,Q,H,D,D), (D,Q,H,D,H), (D,Q,H,D,Q), (D,Q,H,H,D), (D,Q,H,H,H), (D,Q,H,H,Q), (D,Q,H,Q,D), (D,Q,H,Q,H), (D,Q,H,Q,Q), (D,Q,Q,D,D), (D,Q,Q,D,H), (D,Q,Q,D,Q), (D,Q,Q,H,D), (D,Q,Q,H,H), (D,Q,Q,H,Q), (D,Q,Q,Q,D), (D,Q,Q,Q,H), (D,Q,Q,Q,Q), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,D,Q), (H,D,D,H,D), (H,D,D,H,H), (H,D,D,H,Q), (H,D,D,Q,D), (H,D,D,Q,H), (H,D,D,Q,Q), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,D,Q), (H,D,H,H,D), (H,D,H,H,H), (H,D,H,H,Q), (H,D,H,Q,D), (H,D,H,Q,H), (H,D,H,Q,Q), (H,D,Q,D,D), (H,D,Q,D,H), (H,D,Q,D,Q), (H,D,Q,H,D), (H,D,Q,H,H), (H,D,Q,H,Q), (H,D,Q,Q,D), (H,D,Q,Q,H), (H,D,Q,Q,Q), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,D,Q), (H,H,D,H,D), (H,H,D,H,H), (H,H,D,H,Q), (H,H,D,Q,D), (H,H,D,Q,H), (H,H,D,Q,Q), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,D,Q), (H,H,H,H,D), (H,H,H,H,H), (H,H,H,H,Q), (H,H,H,Q,D), (H,H,H,Q,H), (H,H,H,Q,Q), (H,H,Q,D,D), (H,H,Q,D,H), (H,H,Q,D,Q), (H,H,Q,H,D), (H,H,Q,H,H), (H,H,Q,H,Q), (H,H,Q,Q,D), (H,H,Q,Q,H), (H,H,Q,Q,Q), (H,Q,D,D,D), (H,Q,D,D,H), (H,Q,D,D,Q), (H,Q,D,H,D), (H,Q,D,H,H), (H,Q,D,H,Q), (H,Q,D,Q,D), (H,Q,D,Q,H), (H,Q,D,Q,Q), (H,Q,H,D,D), (H,Q,H,D,H), (H,Q,H,D,Q), (H,Q,H,H,D), (H,Q,H,H,H), (H,Q,H,H,Q), (H,Q,H,Q,D), (H,Q,H,Q,H), (H,Q,H,Q,Q), (H,Q,Q,D,D), (H,Q,Q,D,H), (H,Q,Q,D,Q), (H,Q,Q,H,D), (H,Q,Q,H,H), (H,Q,Q,H,Q), (H,Q,Q,Q,D), (H,Q,Q,Q,H), (H,Q,Q,Q,Q), (Q,D,D,D,D), (Q,D,D,D,H), (Q,D,D,D,Q), (Q,D,D,H,D), (Q,D,D,H,H), (Q,D,D,H,Q), (Q,D,D,Q,D), (Q,D,D,Q,H), (Q,D,D,Q,Q), (Q,D,H,D,D), (Q,D,H,D,H), (Q,D,H,D,Q), (Q,D,H,H,D), (Q,D,H,H,H), (Q,D,H,H,Q), (Q,D,H,Q,D), (Q,D,H,Q,H), (Q,D,H,Q,Q), (Q,D,Q,D,D), (Q,D,Q,D,H), (Q,D,Q,D,Q), (Q,D,Q,H,D), (Q,D,Q,H,H), (Q,D,Q,H,Q), (Q,D,Q,Q,D), (Q,D,Q,Q,H), (Q,D,Q,Q,Q), (Q,H,D,D,D), (Q,H,D,D,H), (Q,H,D,D,Q), (Q,H,D,H,D), (Q,H,D,H,H), (Q,H,D,H,Q), (Q,H,D,Q,D), (Q,H,D,Q,H), (Q,H,D,Q,Q), (Q,H,H,D,D), (Q,H,H,D,H), (Q,H,H,D,Q), (Q,H,H,H,D), (Q,H,H,H,H), (Q,H,H,H,Q), (Q,H,H,Q,D), (Q,H,H,Q,H), (Q,H,H,Q,Q), (Q,H,Q,D,D), (Q,H,Q,D,H), (Q,H,Q,D,Q), (Q,H,Q,H,D), (Q,H,Q,H,H), (Q,H,Q,H,Q), (Q,H,Q,Q,D), (Q,H,Q,Q,H), (Q,H,Q,Q,Q), (Q,Q,D,D,D), (Q,Q,D,D,H), (Q,Q,D,D,Q), (Q,Q,D,H,D), (Q,Q,D,H,H), (Q,Q,D,H,Q), (Q,Q,D,Q,D), (Q,Q,D,Q,H), (Q,Q,D,Q,Q), (Q,Q,H,D,D), (Q,Q,H,D,H), (Q,Q,H,D,Q), (Q,Q,H,H,D), (Q,Q,H,H,H), (Q,Q,H,H,Q), (Q,Q,H,Q,D), (Q,Q,H,Q,H), (Q,Q,H,Q,Q), (Q,Q,Q,D,D), (Q,Q,Q,D,H), (Q,Q,Q,D,Q), (Q,Q,Q,H,D), (Q,Q,Q,H,H), (Q,Q,Q,H,Q), (Q,Q,Q,Q,D), (Q,Q,Q,Q,H), (Q,Q,Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | yes |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | yes |

### N=5 · w · gamma=pi/2 · noise p=0.045 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **-0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,H,D), (D,D,D,H,H), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,H,D), (D,D,H,H,H), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,H,D), (D,H,D,H,H), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,H,D), (D,H,H,H,H), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,H,D), (H,D,D,H,H), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,H,D), (H,D,H,H,H), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,H,D), (H,H,D,H,H), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,H,D), (H,H,H,H,H)

All pure NE: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,D,Q), (D,D,D,H,D), (D,D,D,H,H), (D,D,D,H,Q), (D,D,D,Q,D), (D,D,D,Q,H), (D,D,D,Q,Q), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,D,Q), (D,D,H,H,D), (D,D,H,H,H), (D,D,H,H,Q), (D,D,H,Q,D), (D,D,H,Q,H), (D,D,H,Q,Q), (D,D,Q,D,D), (D,D,Q,D,H), (D,D,Q,D,Q), (D,D,Q,H,D), (D,D,Q,H,H), (D,D,Q,H,Q), (D,D,Q,Q,D), (D,D,Q,Q,H), (D,D,Q,Q,Q), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,D,Q), (D,H,D,H,D), (D,H,D,H,H), (D,H,D,H,Q), (D,H,D,Q,D), (D,H,D,Q,H), (D,H,D,Q,Q), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,D,Q), (D,H,H,H,D), (D,H,H,H,H), (D,H,H,H,Q), (D,H,H,Q,D), (D,H,H,Q,H), (D,H,H,Q,Q), (D,H,Q,D,D), (D,H,Q,D,H), (D,H,Q,D,Q), (D,H,Q,H,D), (D,H,Q,H,H), (D,H,Q,H,Q), (D,H,Q,Q,D), (D,H,Q,Q,H), (D,H,Q,Q,Q), (D,Q,D,D,D), (D,Q,D,D,H), (D,Q,D,D,Q), (D,Q,D,H,D), (D,Q,D,H,H), (D,Q,D,H,Q), (D,Q,D,Q,D), (D,Q,D,Q,H), (D,Q,D,Q,Q), (D,Q,H,D,D), (D,Q,H,D,H), (D,Q,H,D,Q), (D,Q,H,H,D), (D,Q,H,H,H), (D,Q,H,H,Q), (D,Q,H,Q,D), (D,Q,H,Q,H), (D,Q,H,Q,Q), (D,Q,Q,D,D), (D,Q,Q,D,H), (D,Q,Q,D,Q), (D,Q,Q,H,D), (D,Q,Q,H,H), (D,Q,Q,H,Q), (D,Q,Q,Q,D), (D,Q,Q,Q,H), (D,Q,Q,Q,Q), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,D,Q), (H,D,D,H,D), (H,D,D,H,H), (H,D,D,H,Q), (H,D,D,Q,D), (H,D,D,Q,H), (H,D,D,Q,Q), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,D,Q), (H,D,H,H,D), (H,D,H,H,H), (H,D,H,H,Q), (H,D,H,Q,D), (H,D,H,Q,H), (H,D,H,Q,Q), (H,D,Q,D,D), (H,D,Q,D,H), (H,D,Q,D,Q), (H,D,Q,H,D), (H,D,Q,H,H), (H,D,Q,H,Q), (H,D,Q,Q,D), (H,D,Q,Q,H), (H,D,Q,Q,Q), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,D,Q), (H,H,D,H,D), (H,H,D,H,H), (H,H,D,H,Q), (H,H,D,Q,D), (H,H,D,Q,H), (H,H,D,Q,Q), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,D,Q), (H,H,H,H,D), (H,H,H,H,H), (H,H,H,H,Q), (H,H,H,Q,D), (H,H,H,Q,H), (H,H,H,Q,Q), (H,H,Q,D,D), (H,H,Q,D,H), (H,H,Q,D,Q), (H,H,Q,H,D), (H,H,Q,H,H), (H,H,Q,H,Q), (H,H,Q,Q,D), (H,H,Q,Q,H), (H,H,Q,Q,Q), (H,Q,D,D,D), (H,Q,D,D,H), (H,Q,D,D,Q), (H,Q,D,H,D), (H,Q,D,H,H), (H,Q,D,H,Q), (H,Q,D,Q,D), (H,Q,D,Q,H), (H,Q,D,Q,Q), (H,Q,H,D,D), (H,Q,H,D,H), (H,Q,H,D,Q), (H,Q,H,H,D), (H,Q,H,H,H), (H,Q,H,H,Q), (H,Q,H,Q,D), (H,Q,H,Q,H), (H,Q,H,Q,Q), (H,Q,Q,D,D), (H,Q,Q,D,H), (H,Q,Q,D,Q), (H,Q,Q,H,D), (H,Q,Q,H,H), (H,Q,Q,H,Q), (H,Q,Q,Q,D), (H,Q,Q,Q,H), (H,Q,Q,Q,Q), (Q,D,D,D,D), (Q,D,D,D,H), (Q,D,D,D,Q), (Q,D,D,H,D), (Q,D,D,H,H), (Q,D,D,H,Q), (Q,D,D,Q,D), (Q,D,D,Q,H), (Q,D,D,Q,Q), (Q,D,H,D,D), (Q,D,H,D,H), (Q,D,H,D,Q), (Q,D,H,H,D), (Q,D,H,H,H), (Q,D,H,H,Q), (Q,D,H,Q,D), (Q,D,H,Q,H), (Q,D,H,Q,Q), (Q,D,Q,D,D), (Q,D,Q,D,H), (Q,D,Q,D,Q), (Q,D,Q,H,D), (Q,D,Q,H,H), (Q,D,Q,H,Q), (Q,D,Q,Q,D), (Q,D,Q,Q,H), (Q,D,Q,Q,Q), (Q,H,D,D,D), (Q,H,D,D,H), (Q,H,D,D,Q), (Q,H,D,H,D), (Q,H,D,H,H), (Q,H,D,H,Q), (Q,H,D,Q,D), (Q,H,D,Q,H), (Q,H,D,Q,Q), (Q,H,H,D,D), (Q,H,H,D,H), (Q,H,H,D,Q), (Q,H,H,H,D), (Q,H,H,H,H), (Q,H,H,H,Q), (Q,H,H,Q,D), (Q,H,H,Q,H), (Q,H,H,Q,Q), (Q,H,Q,D,D), (Q,H,Q,D,H), (Q,H,Q,D,Q), (Q,H,Q,H,D), (Q,H,Q,H,H), (Q,H,Q,H,Q), (Q,H,Q,Q,D), (Q,H,Q,Q,H), (Q,H,Q,Q,Q), (Q,Q,D,D,D), (Q,Q,D,D,H), (Q,Q,D,D,Q), (Q,Q,D,H,D), (Q,Q,D,H,H), (Q,Q,D,H,Q), (Q,Q,D,Q,D), (Q,Q,D,Q,H), (Q,Q,D,Q,Q), (Q,Q,H,D,D), (Q,Q,H,D,H), (Q,Q,H,D,Q), (Q,Q,H,H,D), (Q,Q,H,H,H), (Q,Q,H,H,Q), (Q,Q,H,Q,D), (Q,Q,H,Q,H), (Q,Q,H,Q,Q), (Q,Q,Q,D,D), (Q,Q,Q,D,H), (Q,Q,Q,D,Q), (Q,Q,Q,H,D), (Q,Q,Q,H,H), (Q,Q,Q,H,Q), (Q,Q,Q,Q,D), (Q,Q,Q,Q,H), (Q,Q,Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | yes |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | yes |

### N=5 · w · gamma=pi/2 · noise p=0.05 (V=4, C=3)

_W noise results are **approximate**: the W entangler's gate-level circuit is transpiler synthesis, not a physical W-prep circuit (Month-4 spec D2)._

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.781250**
- Classical NE mean payoff: **0.781250**
- Advantage (QNE − CNE, mean): **-0.000000**
- (Q,Q,Q,Q,Q) is pure Nash: **True**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,H,D), (D,D,D,H,H), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,H,D), (D,D,H,H,H), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,H,D), (D,H,D,H,H), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,H,D), (D,H,H,H,H), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,H,D), (H,D,D,H,H), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,H,D), (H,D,H,H,H), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,H,D), (H,H,D,H,H), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,H,D), (H,H,H,H,H)

All pure NE: (D,D,D,D,D), (D,D,D,D,H), (D,D,D,D,Q), (D,D,D,H,D), (D,D,D,H,H), (D,D,D,H,Q), (D,D,D,Q,D), (D,D,D,Q,H), (D,D,D,Q,Q), (D,D,H,D,D), (D,D,H,D,H), (D,D,H,D,Q), (D,D,H,H,D), (D,D,H,H,H), (D,D,H,H,Q), (D,D,H,Q,D), (D,D,H,Q,H), (D,D,H,Q,Q), (D,D,Q,D,D), (D,D,Q,D,H), (D,D,Q,D,Q), (D,D,Q,H,D), (D,D,Q,H,H), (D,D,Q,H,Q), (D,D,Q,Q,D), (D,D,Q,Q,H), (D,D,Q,Q,Q), (D,H,D,D,D), (D,H,D,D,H), (D,H,D,D,Q), (D,H,D,H,D), (D,H,D,H,H), (D,H,D,H,Q), (D,H,D,Q,D), (D,H,D,Q,H), (D,H,D,Q,Q), (D,H,H,D,D), (D,H,H,D,H), (D,H,H,D,Q), (D,H,H,H,D), (D,H,H,H,H), (D,H,H,H,Q), (D,H,H,Q,D), (D,H,H,Q,H), (D,H,H,Q,Q), (D,H,Q,D,D), (D,H,Q,D,H), (D,H,Q,D,Q), (D,H,Q,H,D), (D,H,Q,H,H), (D,H,Q,H,Q), (D,H,Q,Q,D), (D,H,Q,Q,H), (D,H,Q,Q,Q), (D,Q,D,D,D), (D,Q,D,D,H), (D,Q,D,D,Q), (D,Q,D,H,D), (D,Q,D,H,H), (D,Q,D,H,Q), (D,Q,D,Q,D), (D,Q,D,Q,H), (D,Q,D,Q,Q), (D,Q,H,D,D), (D,Q,H,D,H), (D,Q,H,D,Q), (D,Q,H,H,D), (D,Q,H,H,H), (D,Q,H,H,Q), (D,Q,H,Q,D), (D,Q,H,Q,H), (D,Q,H,Q,Q), (D,Q,Q,D,D), (D,Q,Q,D,H), (D,Q,Q,D,Q), (D,Q,Q,H,D), (D,Q,Q,H,H), (D,Q,Q,H,Q), (D,Q,Q,Q,D), (D,Q,Q,Q,H), (D,Q,Q,Q,Q), (H,D,D,D,D), (H,D,D,D,H), (H,D,D,D,Q), (H,D,D,H,D), (H,D,D,H,H), (H,D,D,H,Q), (H,D,D,Q,D), (H,D,D,Q,H), (H,D,D,Q,Q), (H,D,H,D,D), (H,D,H,D,H), (H,D,H,D,Q), (H,D,H,H,D), (H,D,H,H,H), (H,D,H,H,Q), (H,D,H,Q,D), (H,D,H,Q,H), (H,D,H,Q,Q), (H,D,Q,D,D), (H,D,Q,D,H), (H,D,Q,D,Q), (H,D,Q,H,D), (H,D,Q,H,H), (H,D,Q,H,Q), (H,D,Q,Q,D), (H,D,Q,Q,H), (H,D,Q,Q,Q), (H,H,D,D,D), (H,H,D,D,H), (H,H,D,D,Q), (H,H,D,H,D), (H,H,D,H,H), (H,H,D,H,Q), (H,H,D,Q,D), (H,H,D,Q,H), (H,H,D,Q,Q), (H,H,H,D,D), (H,H,H,D,H), (H,H,H,D,Q), (H,H,H,H,D), (H,H,H,H,H), (H,H,H,H,Q), (H,H,H,Q,D), (H,H,H,Q,H), (H,H,H,Q,Q), (H,H,Q,D,D), (H,H,Q,D,H), (H,H,Q,D,Q), (H,H,Q,H,D), (H,H,Q,H,H), (H,H,Q,H,Q), (H,H,Q,Q,D), (H,H,Q,Q,H), (H,H,Q,Q,Q), (H,Q,D,D,D), (H,Q,D,D,H), (H,Q,D,D,Q), (H,Q,D,H,D), (H,Q,D,H,H), (H,Q,D,H,Q), (H,Q,D,Q,D), (H,Q,D,Q,H), (H,Q,D,Q,Q), (H,Q,H,D,D), (H,Q,H,D,H), (H,Q,H,D,Q), (H,Q,H,H,D), (H,Q,H,H,H), (H,Q,H,H,Q), (H,Q,H,Q,D), (H,Q,H,Q,H), (H,Q,H,Q,Q), (H,Q,Q,D,D), (H,Q,Q,D,H), (H,Q,Q,D,Q), (H,Q,Q,H,D), (H,Q,Q,H,H), (H,Q,Q,H,Q), (H,Q,Q,Q,D), (H,Q,Q,Q,H), (H,Q,Q,Q,Q), (Q,D,D,D,D), (Q,D,D,D,H), (Q,D,D,D,Q), (Q,D,D,H,D), (Q,D,D,H,H), (Q,D,D,H,Q), (Q,D,D,Q,D), (Q,D,D,Q,H), (Q,D,D,Q,Q), (Q,D,H,D,D), (Q,D,H,D,H), (Q,D,H,D,Q), (Q,D,H,H,D), (Q,D,H,H,H), (Q,D,H,H,Q), (Q,D,H,Q,D), (Q,D,H,Q,H), (Q,D,H,Q,Q), (Q,D,Q,D,D), (Q,D,Q,D,H), (Q,D,Q,D,Q), (Q,D,Q,H,D), (Q,D,Q,H,H), (Q,D,Q,H,Q), (Q,D,Q,Q,D), (Q,D,Q,Q,H), (Q,D,Q,Q,Q), (Q,H,D,D,D), (Q,H,D,D,H), (Q,H,D,D,Q), (Q,H,D,H,D), (Q,H,D,H,H), (Q,H,D,H,Q), (Q,H,D,Q,D), (Q,H,D,Q,H), (Q,H,D,Q,Q), (Q,H,H,D,D), (Q,H,H,D,H), (Q,H,H,D,Q), (Q,H,H,H,D), (Q,H,H,H,H), (Q,H,H,H,Q), (Q,H,H,Q,D), (Q,H,H,Q,H), (Q,H,H,Q,Q), (Q,H,Q,D,D), (Q,H,Q,D,H), (Q,H,Q,D,Q), (Q,H,Q,H,D), (Q,H,Q,H,H), (Q,H,Q,H,Q), (Q,H,Q,Q,D), (Q,H,Q,Q,H), (Q,H,Q,Q,Q), (Q,Q,D,D,D), (Q,Q,D,D,H), (Q,Q,D,D,Q), (Q,Q,D,H,D), (Q,Q,D,H,H), (Q,Q,D,H,Q), (Q,Q,D,Q,D), (Q,Q,D,Q,H), (Q,Q,D,Q,Q), (Q,Q,H,D,D), (Q,Q,H,D,H), (Q,Q,H,D,Q), (Q,Q,H,H,D), (Q,Q,H,H,H), (Q,Q,H,H,Q), (Q,Q,H,Q,D), (Q,Q,H,Q,H), (Q,Q,H,Q,Q), (Q,Q,Q,D,D), (Q,Q,Q,D,H), (Q,Q,Q,D,Q), (Q,Q,Q,H,D), (Q,Q,Q,H,H), (Q,Q,Q,H,Q), (Q,Q,Q,Q,D), (Q,Q,Q,Q,H), (Q,Q,Q,Q,Q)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.781250 | 0.781250 | yes |
| player 0 | H | 0.781250 | 0.781250 | yes |
| player 1 | D | 0.781250 | 0.781250 | yes |
| player 1 | H | 0.781250 | 0.781250 | yes |
| player 2 | D | 0.781250 | 0.781250 | yes |
| player 2 | H | 0.781250 | 0.781250 | yes |
| player 3 | D | 0.781250 | 0.781250 | yes |
| player 3 | H | 0.781250 | 0.781250 | yes |
| player 4 | D | 0.781250 | 0.781250 | yes |
| player 4 | H | 0.781250 | 0.781250 | yes |

### N=5 · ring · gamma=pi/2 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.800000**
- Classical NE mean payoff: **0.200000**
- Advantage (QNE − CNE, mean): **0.600000**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **True**

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.895067 | 0.800000 | **NO — NASH VIOLATED** |
| player 0 | H | 1.161738 | 0.800000 | **NO — NASH VIOLATED** |
| player 1 | D | 0.895067 | 0.800000 | **NO — NASH VIOLATED** |
| player 1 | H | 1.161738 | 0.800000 | **NO — NASH VIOLATED** |
| player 2 | D | 0.895067 | 0.800000 | **NO — NASH VIOLATED** |
| player 2 | H | 1.161738 | 0.800000 | **NO — NASH VIOLATED** |
| player 3 | D | 0.895067 | 0.800000 | **NO — NASH VIOLATED** |
| player 3 | H | 1.161738 | 0.800000 | **NO — NASH VIOLATED** |
| player 4 | D | 0.895067 | 0.800000 | **NO — NASH VIOLATED** |
| player 4 | H | 1.161738 | 0.800000 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.005 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.796221**
- Classical NE mean payoff: **0.323823**
- Advantage (QNE − CNE, mean): **0.472398**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7995, 0.7986, 0.7959, 0.7938, 0.7933]
- Classical NE payoff vector: [0.3022, 0.3117, 0.3230, 0.3409, 0.3412]
- Advantage vector: [0.4973, 0.4869, 0.4729, 0.4528, 0.4521]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.881041 | 0.799506 | **NO — NASH VIOLATED** |
| player 0 | H | 1.093407 | 0.799506 | **NO — NASH VIOLATED** |
| player 1 | D | 0.878775 | 0.798601 | **NO — NASH VIOLATED** |
| player 1 | H | 1.092380 | 0.798601 | **NO — NASH VIOLATED** |
| player 2 | D | 0.876945 | 0.795942 | **NO — NASH VIOLATED** |
| player 2 | H | 1.095005 | 0.795942 | **NO — NASH VIOLATED** |
| player 3 | D | 0.875509 | 0.793759 | **NO — NASH VIOLATED** |
| player 3 | H | 1.097247 | 0.793759 | **NO — NASH VIOLATED** |
| player 4 | D | 0.873699 | 0.793296 | **NO — NASH VIOLATED** |
| player 4 | H | 1.095836 | 0.793296 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.01 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.793244**
- Classical NE mean payoff: **0.420919**
- Advantage (QNE − CNE, mean): **0.372324**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7988, 0.7973, 0.7928, 0.7890, 0.7883]
- Classical NE payoff vector: [0.3834, 0.3992, 0.4190, 0.4510, 0.4519]
- Advantage vector: [0.4154, 0.3981, 0.3738, 0.3380, 0.3364]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.868716 | 0.798773 | **NO — NASH VIOLATED** |
| player 0 | H | 1.037789 | 0.798773 | **NO — NASH VIOLATED** |
| player 1 | D | 0.864852 | 0.797299 | **NO — NASH VIOLATED** |
| player 1 | H | 1.035979 | 0.797299 | **NO — NASH VIOLATED** |
| player 2 | D | 0.861911 | 0.792837 | **NO — NASH VIOLATED** |
| player 2 | H | 1.040494 | 0.792837 | **NO — NASH VIOLATED** |
| player 3 | D | 0.859391 | 0.789015 | **NO — NASH VIOLATED** |
| player 3 | H | 1.044385 | 0.789015 | **NO — NASH VIOLATED** |
| player 4 | D | 0.856377 | 0.788294 | **NO — NASH VIOLATED** |
| player 4 | H | 1.042002 | 0.788294 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.015 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.790893**
- Classical NE mean payoff: **0.497089**
- Advantage (QNE − CNE, mean): **0.293804**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7979, 0.7961, 0.7905, 0.7854, 0.7846]
- Classical NE payoff vector: [0.4482, 0.4680, 0.4940, 0.5368, 0.5384]
- Advantage vector: [0.3497, 0.3281, 0.2964, 0.2487, 0.2462]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.857887 | 0.797874 | **NO — NASH VIOLATED** |
| player 0 | H | 0.992449 | 0.797874 | **NO — NASH VIOLATED** |
| player 1 | D | 0.852945 | 0.796073 | **NO — NASH VIOLATED** |
| player 1 | H | 0.990060 | 0.796073 | **NO — NASH VIOLATED** |
| player 2 | D | 0.849409 | 0.790462 | **NO — NASH VIOLATED** |
| player 2 | H | 0.995879 | 0.790462 | **NO — NASH VIOLATED** |
| player 3 | D | 0.846090 | 0.785448 | **NO — NASH VIOLATED** |
| player 3 | H | 1.000934 | 0.785448 | **NO — NASH VIOLATED** |
| player 4 | D | 0.842324 | 0.784607 | **NO — NASH VIOLATED** |
| player 4 | H | 0.997919 | 0.784607 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.02 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.789031**
- Classical NE mean payoff: **0.556873**
- Advantage (QNE − CNE, mean): **0.232158**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7969, 0.7949, 0.7886, 0.7828, 0.7819]
- Classical NE payoff vector: [0.5004, 0.5224, 0.5527, 0.6033, 0.6056]
- Advantage vector: [0.2964, 0.2725, 0.2360, 0.1795, 0.1764]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.848375 | 0.796868 | **NO — NASH VIOLATED** |
| player 0 | H | 0.955427 | 0.796868 | **NO — NASH VIOLATED** |
| player 1 | D | 0.842754 | 0.794911 | **NO — NASH VIOLATED** |
| player 1 | H | 0.952631 | 0.794911 | **NO — NASH VIOLATED** |
| player 2 | D | 0.838987 | 0.788645 | **NO — NASH VIOLATED** |
| player 2 | H | 0.959289 | 0.788645 | **NO — NASH VIOLATED** |
| player 3 | D | 0.835097 | 0.782802 | **NO — NASH VIOLATED** |
| player 3 | H | 0.965118 | 0.782802 | **NO — NASH VIOLATED** |
| player 4 | D | 0.830914 | 0.781931 | **NO — NASH VIOLATED** |
| player 4 | H | 0.961730 | 0.781931 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.025 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.787553**
- Classical NE mean payoff: **0.603827**
- Advantage (QNE − CNE, mean): **0.183726**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7958, 0.7938, 0.7873, 0.7809, 0.7800]
- Classical NE payoff vector: [0.5429, 0.5657, 0.5986, 0.6546, 0.6575]
- Advantage vector: [0.2529, 0.2281, 0.1887, 0.1263, 0.1226]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.840023 | 0.795801 | **NO — NASH VIOLATED** |
| player 0 | H | 0.925149 | 0.795801 | **NO — NASH VIOLATED** |
| player 1 | D | 0.834027 | 0.793809 | **NO — NASH VIOLATED** |
| player 1 | H | 0.922086 | 0.793809 | **NO — NASH VIOLATED** |
| player 2 | D | 0.830277 | 0.787251 | **NO — NASH VIOLATED** |
| player 2 | H | 0.929219 | 0.787251 | **NO — NASH VIOLATED** |
| player 3 | D | 0.826000 | 0.780874 | **NO — NASH VIOLATED** |
| player 3 | H | 0.935512 | 0.780874 | **NO — NASH VIOLATED** |
| player 4 | D | 0.821644 | 0.780030 | **NO — NASH VIOLATED** |
| player 4 | H | 0.931947 | 0.780030 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.03 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.786376**
- Classical NE mean payoff: **0.640734**
- Advantage (QNE − CNE, mean): **0.145642**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7947, 0.7928, 0.7862, 0.7795, 0.7787]
- Classical NE payoff vector: [0.5776, 0.6003, 0.6345, 0.6939, 0.6973]
- Advantage vector: [0.2171, 0.1924, 0.1517, 0.0856, 0.0814]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.832690 | 0.794711 | **NO — NASH VIOLATED** |
| player 0 | H | 0.900342 | 0.794711 | **NO — NASH VIOLATED** |
| player 1 | D | 0.826548 | 0.792764 | **NO — NASH VIOLATED** |
| player 1 | H | 0.897126 | 0.792764 | **NO — NASH VIOLATED** |
| player 2 | D | 0.822979 | 0.786178 | **NO — NASH VIOLATED** |
| player 2 | H | 0.904456 | 0.786178 | **NO — NASH VIOLATED** |
| player 3 | D | 0.818463 | 0.779504 | **NO — NASH VIOLATED** |
| player 3 | H | 0.910969 | 0.779504 | **NO — NASH VIOLATED** |
| player 4 | D | 0.814107 | 0.778720 | **NO — NASH VIOLATED** |
| player 4 | H | 0.907371 | 0.778720 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.035 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.785434**
- Classical NE mean payoff: **0.669771**
- Advantage (QNE − CNE, mean): **0.115664**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7936, 0.7918, 0.7853, 0.7786, 0.7779]
- Classical NE payoff vector: [0.6063, 0.6282, 0.6628, 0.7239, 0.7276]
- Advantage vector: [0.1873, 0.1635, 0.1226, 0.0547, 0.0503]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.826255 | 0.793625 | **NO — NASH VIOLATED** |
| player 0 | H | 0.879983 | 0.793625 | **NO — NASH VIOLATED** |
| player 1 | D | 0.820136 | 0.791775 | **NO — NASH VIOLATED** |
| player 1 | H | 0.876706 | 0.791775 | **NO — NASH VIOLATED** |
| player 2 | D | 0.816848 | 0.785350 | **NO — NASH VIOLATED** |
| player 2 | H | 0.884020 | 0.785350 | **NO — NASH VIOLATED** |
| player 3 | D | 0.812212 | 0.778564 | **NO — NASH VIOLATED** |
| player 3 | H | 0.890567 | 0.778564 | **NO — NASH VIOLATED** |
| player 4 | D | 0.807978 | 0.777858 | **NO — NASH VIOLATED** |
| player 4 | H | 0.887040 | 0.777858 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.04 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.784679**
- Classical NE mean payoff: **0.692640**
- Advantage (QNE − CNE, mean): **0.092039**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7926, 0.7908, 0.7847, 0.7780, 0.7773]
- Classical NE payoff vector: [0.6303, 0.6510, 0.6851, 0.7465, 0.7504]
- Advantage vector: [0.1623, 0.1399, 0.0996, 0.0314, 0.0270]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.820609 | 0.792564 | **NO — NASH VIOLATED** |
| player 0 | H | 0.863246 | 0.792564 | **NO — NASH VIOLATED** |
| player 1 | D | 0.814637 | 0.790842 | **NO — NASH VIOLATED** |
| player 1 | H | 0.859978 | 0.790842 | **NO — NASH VIOLATED** |
| player 2 | D | 0.811684 | 0.784705 | **NO — NASH VIOLATED** |
| player 2 | H | 0.867122 | 0.784705 | **NO — NASH VIOLATED** |
| player 3 | D | 0.807022 | 0.777953 | **NO — NASH VIOLATED** |
| player 3 | H | 0.873561 | 0.777953 | **NO — NASH VIOLATED** |
| player 4 | D | 0.802989 | 0.777331 | **NO — NASH VIOLATED** |
| player 4 | H | 0.870176 | 0.777331 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.045 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.784071**
- Classical NE mean payoff: **0.710675**
- Advantage (QNE − CNE, mean): **0.073396**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7915, 0.7900, 0.7842, 0.7776, 0.7771]
- Classical NE payoff vector: [0.6505, 0.6696, 0.7026, 0.7634, 0.7673]
- Advantage vector: [0.1411, 0.1204, 0.0816, 0.0142, 0.0098]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.815656 | 0.791543 | **NO — NASH VIOLATED** |
| player 0 | H | 0.849460 | 0.791543 | **NO — NASH VIOLATED** |
| player 1 | D | 0.809918 | 0.789966 | **NO — NASH VIOLATED** |
| player 1 | H | 0.846257 | 0.789966 | **NO — NASH VIOLATED** |
| player 2 | D | 0.807323 | 0.784199 | **NO — NASH VIOLATED** |
| player 2 | H | 0.853120 | 0.784199 | **NO — NASH VIOLATED** |
| player 3 | D | 0.802709 | 0.777592 | **NO — NASH VIOLATED** |
| player 3 | H | 0.859347 | 0.777592 | **NO — NASH VIOLATED** |
| player 4 | D | 0.798929 | 0.777053 | **NO — NASH VIOLATED** |
| player 4 | H | 0.856154 | 0.777053 | **NO — NASH VIOLATED** |

### N=5 · ring · gamma=pi/2 · noise p=0.05 (V=4, C=3)

- (Q,Q,Q,Q,Q) mean per-player payoff: **0.783579**
- Classical NE mean payoff: **0.724917**
- Advantage (QNE − CNE, mean): **0.058662**
- (Q,Q,Q,Q,Q) is pure Nash: **False**
- Player-symmetric: **False**

**Per-player breakdown (asymmetric topology):**

- Q payoff vector: [0.7906, 0.7891, 0.7838, 0.7774, 0.7770]
- Classical NE payoff vector: [0.6675, 0.6850, 0.7166, 0.7758, 0.7796]
- Advantage vector: [0.1230, 0.1041, 0.0672, 0.0016, -0.0027]

Classical pure NE in {D,H}^N: (H,H,H,H,H)

All pure NE: (H,H,H,H,H)

Unilateral deviation table from (Q,...,Q):

| deviator | alt | dev payoff | Q payoff | Q dominates |
|---|---|---|---|---|
| player 0 | D | 0.811314 | 0.790572 | **NO — NASH VIOLATED** |
| player 0 | H | 0.838086 | 0.790572 | **NO — NASH VIOLATED** |
| player 1 | D | 0.805867 | 0.789147 | **NO — NASH VIOLATED** |
| player 1 | H | 0.834989 | 0.789147 | **NO — NASH VIOLATED** |
| player 2 | D | 0.803630 | 0.783798 | **NO — NASH VIOLATED** |
| player 2 | H | 0.841495 | 0.783798 | **NO — NASH VIOLATED** |
| player 3 | D | 0.799122 | 0.777419 | **NO — NASH VIOLATED** |
| player 3 | H | 0.847436 | 0.777419 | **NO — NASH VIOLATED** |
| player 4 | D | 0.795622 | 0.776958 | **NO — NASH VIOLATED** |
| player 4 | H | 0.844463 | 0.776958 | **NO — NASH VIOLATED** |

## Data files

- `results.json` — full structured results
- `results.csv` — one row per cell
- `config.snapshot.yaml` — exact parameters used
