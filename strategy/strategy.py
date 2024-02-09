class BasicStrategy:
    def __init__(self, history: list, lcl: float, volk: float):
        self.history = history
        self.len = len(history)
        self.lcl = lcl
        self.volk = volk
        self.volatility = 0
        for i in range(self.len - 1):
            self.volatility += abs(history[i + 1] - history[i])
        self.volatility /= self.len - 1

    def predict_range(self, k: int):
        vals = self.history[self.len - k:self.len]
        local_volatility = 0
        for i in range(len(vals) - 1):
            local_volatility += abs(vals[i + 1] - vals[i])
        local_volatility /= len(vals) - 1
        v = (self.lcl * local_volatility + self.volatility) / (1 + self.lcl)
        local_delta = (vals[len(vals) - 1] - vals[0]) / (len(vals) - 1)
        next = self.history[self.len - 1] + local_delta
        return next - v * self.volk, next + v * self.volk

    def predict(self, k_from: int = 3, k_to: int = 500):
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

    def predict_percent(self, k_from: int = 3, k_to: int = 500):
        last = self.history[len(self.history) - 1]
        return (self.predict(k_from, k_to) / last - 1) * 100

    def predict1(self, k_from: int = 3, k_to: int = 10):
        cnt = 0
        ans1 = 0
        ans2 = 0
        for k in range(k_from, k_to + 1):
            if k > self.len:
                break
            cnt += 1
            r = self.predict_range(k)
            ans1 += r[0]
            ans2 += r[1]
        ans1 /= cnt
        ans2 /= cnt
        return ans1, ans2

    def predict_percent1(self, k_from: int = 3, k_to: int = 500):
        last = self.history[self.len - 1]
        left_board, right_board = self.predict1(k_from, k_to)
        mid = (left_board + right_board) / 2
        prediction = 0
        if (left_board >= last):
            prediction = 1
        elif (right_board <= last):
            prediction = -1
        else:
            prediction = (mid - last) / (right_board - mid)
        return prediction

    def long_prediction(self, m = 1, k_from: int = 3, k_to: int = 500):
        for i in range(m):
            a, b = self.predict1()
            self.history.append((a + b) / 2)
            self.len += 1;
        res = self.history[self.len - m:self.len]
        self.len -= m;
        self.history = self.history[:self.len]
        return res


def get_strategy(h: list):
    return BasicStrategy(h, 10.0, 0.25)


def mr_strategy(history, f, s, mx):
    n = len(history)
    savg = [0 for i in range(n)]
    favg = [0 for i in range(n)]
    s_sum = 0
    for i in range(s):
        s_sum += history[i]
    f_sum = 0
    for i in range(f):
        f_sum += history[i]
    for i in range(s - 1, n):
        if i != s - 1:
            s_sum = s_sum - history[i - s] + history[i]
        savg[i] = s_sum / s
    for i in range(f - 1, n):
        if i != f - 1:
            f_sum = f_sum - history[i - f] + history[i]
        favg[i] = f_sum / f
    revs = [(0, 1)]
    for i in range(1, n):
        sgn0 = 1 if savg[i - 1] - favg[i - 1] >= 0 else -1
        sgn1 = 1 if savg[i] - favg[i] >= 0 else -1
        if sgn0 != sgn1:
            revs.append((i, sgn1))
    sgn = revs[len(revs) - 1][1]
    if revs[len(revs) - 1][0] == n - 1:
        return 1.0 * sgn
    diff = min(abs(savg[n - 1] - favg[n - 1]) / mx, 1.0)
    return -1.0 * sgn * (1.0 - diff)