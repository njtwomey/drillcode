Packages with the given `weights` sit on a conveyor belt and must be shipped, in the order given, within `days` days. Each day the ship is loaded with consecutive packages from the belt, never exceeding its fixed weight capacity. Return the smallest capacity that lets every package ship within `days` days.

Constraints:
- `1 <= days <= len(weights) <= 5 * 10^4`
- `1 <= weights[i] <= 500`
- Packages cannot be reordered or split across days
