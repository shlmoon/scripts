# coding: utf-8

MaxCost = 10000


class Dkalgorithm(object):

    def __init__(self, rule={}, source='', nodes=[]):
        super(Dkalgorithm, self).__init__()
        self.rules = rule if rule else {}
        self.min_cost = {source: {}}
        self.step = {source: {}}
        self.nodes = nodes
        self.source = source

    def djkstraAlg(self, S, V):
        # S 不一定等于self.nodes，除了node之外，还有顺序。
        if S == self.nodes or V == []:
            return

        minsv = MaxCost
        select_vnode = None
        select_snode = None

        if S == []:
            select_snode = self.source
            for vnode in V:
                if minsv > self.rules.get(self.source).get(vnode):
                    minsv = self.rules.get(self.source).get(vnode)
                    select_vnode = vnode
        else:
            for snode in S:
                for vnode in V:
                    if minsv > self.rules.get(snode).get(
                            vnode) + self.min_cost.get(self.source).get(snode, 0):

                        minsv = self.rules.get(snode).get(
                            vnode) + self.min_cost.get(self.source).get(snode, 0)
                        select_vnode = vnode
                        select_snode = snode

        if not self.step.get(self.source).get(select_snode, None) is None:
            self.step.get(self.source)[select_vnode] = '%s-%s' % (
                self.step.get(self.source)[select_snode],
                select_vnode
            )
        else:
            self.step.get(
                self.source)[select_vnode] = '%s-%s' % (
                select_snode,
                select_vnode
            )

        self.min_cost.get(self.source)[select_vnode] = minsv
        S.append(select_vnode)
        V.remove(select_vnode)
        self.djkstraAlg(S, V)

    def run(self):
        self.djkstraAlg([self.source],
                        [x for x in self.nodes if not x == self.source])
