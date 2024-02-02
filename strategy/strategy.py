class BasicStrategy:
    def __init__(self, history: list, lcl: float, volk: float):
        self.history = history
        self.lcl = lcl
        self.volk = volk
        deriv = []
        for i in range(len(history) - 1):
            deriv.append(history[i + 1] - history[i])
        self.volatility = 0
        for i in range(len(deriv)):
            self.volatility += abs(deriv[i])
        self.volatility /= len(deriv)

    def predict_range(self, k: int):
        vals = []
        for i in range(k):
            vals.append(self.history[len(self.history) - 1 - i])
        vals.reverse()
        deriv = []
        for i in range(len(vals) - 1):
            deriv.append(vals[i + 1] - vals[i])
        local_volatility = 0
        for i in range(len(deriv)):
            local_volatility += abs(deriv[i])
        local_volatility /= len(deriv)
        v = (self.lcl * local_volatility + self.volatility) / (1 + self.lcl)
        local_delta = (vals[len(vals) - 1] - vals[0]) / (len(vals) - 1)
        next = self.history[len(self.history) - 1] + local_delta
        return next - v * self.volk, next + v * self.volk

    def predict(self, k_from: int = 3, k_to: int = 10):
        cnt = 0
        ans = 0
        for k in range(k_from, k_to + 1):
            if k > len(self.history):
                break
            cnt += 1
            r = self.predict_range(k)
            p = (r[0] + r[1]) * 0.5
            ans += p
        return ans / cnt

    def predict_percent(self, k_from: int = 3, k_to: int = 10):
        last = self.history[len(self.history) - 1]
        return (self.predict(k_from, k_to) / last - 1) * 100


def get_strategy(h: list):
    return BasicStrategy(h, 10.0, 0.25)
