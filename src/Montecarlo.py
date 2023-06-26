import time

class Montecarlo:

    def __init__(self, limit, count):
        self.limit = limit
        self.count = count
        self.transposition_table = {}

    def findbestmove(self, role, match):
        actions = match.findlegals(role)
        action = actions[0]
        score = 0
        start_time = time.time()
        if len(actions) == 1:
            return action
        for i in range(0, len(actions)):
            if match.pc:
                if match.pc < time.time() - start_time:
                    return action
            result = self.minscore(role, actions[i], match, 0, 0, 100)
            if result == 100:
                return actions[i]
            elif result > score:
                score = result
                action = actions[i]
        return action

    def minscore(self, role, action, match, level, alpha, beta):
        opponent = self.findopponent(role, match)
        actions = match.findlegals(opponent)
        for i in range(len(actions)):
            move = []
            if role == match.roles[0]:
                move = [action, actions[i]]
            else:
                move = [actions[i], action]
            newmatch = match.simulate(move)
            if newmatch.get_state_str() in self.transposition_table:
                return self.transposition_table[newmatch.get_state_str()]
            result = self.maxscore(role, newmatch, level+1, alpha, beta)
            if result < beta:
                beta = result
            if beta <=alpha:
                self.transposition_table[match.get_state_str()] = alpha
                return alpha
        self.transposition_table[match.get_state_str()] = beta
        return beta
        
    def maxscore(self, role, match, level, alpha, beta):
        if match.findterminalp():
            return match.findreward(role)
        if match.get_state_str() in self.transposition_table:
            return self.transposition_table[match.get_state_str()]
        if level >= self.limit:
            montecarlo_score = self.montecarlo(role, match, self.count)
            self.transposition_table[match.get_state_str()] = montecarlo_score
            return montecarlo_score
        actions = match.findlegals(role)
        for i in range(len(actions)):
            result = self.minscore(role, actions[i], match, level, alpha, beta)
            if result > alpha:
                alpha = result
            if alpha >= beta:
                self.transposition_table[match.get_state_str()] = beta
                return beta
        self.transposition_table[match.get_state_str()] = alpha
        return alpha

    def findopponent(self, role, match):
        for other_role in match.roles:
            if other_role != role:
                return other_role
            
    def montecarlo(self, role, state, count):
        total = 0
        for _ in range(count):
            total = total + self.depthcharge(role,state)
        return total/count

    def depthcharge(self, role, state):
        if state.findterminalp():
            return state.findreward(role)
        move = []
        for i in range(len(state.roles)):
            move.append(state.findlegalr(state.roles[i]))
        newstate = state.simulate(move)
        return self.depthcharge(role, newstate)