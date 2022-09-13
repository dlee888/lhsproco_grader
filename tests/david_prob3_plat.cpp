#include <bits/stdc++.h>

using namespace std;

const int inf = 1e9 + 7;

class SegtreeNode {
  public:
	int value;
	int lazy;

	SegtreeNode() {
		value = -inf;
		lazy = 0;
	}
	SegtreeNode(int val) {
		value = val;
		lazy = 0;
	}

	void update(int val, int node_left, int node_right) {
		value += val;
		lazy += val;
	}

	void merge(SegtreeNode x) { value = max(x.value, value); }
};

class SegTree {
  public:
	int size;
	vector<SegtreeNode> nodes;

	SegTree(int n) {
		nodes = vector<SegtreeNode>(4 * n, SegtreeNode(0));
		size = n;
	}

	void lazy_prop(int node, int node_left, int node_right) {
		int node_mid = node_left + (node_right - node_left) / 2;
		nodes[2 * node].update(nodes[node].lazy, node_left, node_mid);
		nodes[2 * node + 1].update(nodes[node].lazy, node_mid + 1, node_right);
		nodes[node].lazy = 0;
	}

	void merge(int node) {
		nodes[node] = SegtreeNode();
		nodes[node].merge(nodes[2 * node]);
		nodes[node].merge(nodes[2 * node + 1]);
	}

	void _update(int node, int node_left, int node_right, int update_left, int update_right, int val) {
		if (node_left >= update_left && node_right <= update_right) {
			nodes[node].update(val, node_left, node_right);
			return;
		}
		lazy_prop(node, node_left, node_right);
		int node_mid = node_left + (node_right - node_left) / 2;
		if (update_left <= node_mid) {
			_update(2 * node, node_left, node_mid, update_left, update_right, val);
		}
		if (update_right > node_mid) {
			_update(2 * node + 1, node_mid + 1, node_right, update_left, update_right, val);
		}
		merge(node);
	}

	void update(int update_left, int update_right, int val) { _update(1, 0, size - 1, update_left, update_right, val); }

	SegtreeNode _query(int node, int node_left, int node_right, int query_left, int query_right) {
		if (node_left >= query_left && node_right <= query_right) {
			return nodes[node];
		}
		lazy_prop(node, node_left, node_right);
		int node_mid = node_left + (node_right - node_left) / 2;
		SegtreeNode res = SegtreeNode();
		if (query_left <= node_mid) {
			res.merge(_query(2 * node, node_left, node_mid, query_left, query_right));
		}
		if (query_right > node_mid) {
			res.merge(_query(2 * node + 1, node_mid + 1, node_right, query_left, query_right));
		}
		return res;
	}

	SegtreeNode query(int query_left, int query_right) { return _query(1, 0, size - 1, query_left, query_right); }

	void debug() {
		for (int i = 0; i < size; i++) {
			cout << query(i, i).value << " ";
		}
		cout << endl;
	}
};

int main() {
	int n;
	cin >> n;
	vector<int> nums(n);
	for (int i = 0; i < n; i++) {
		cin >> nums[i];
		nums[i]--;
	}
	vector<bool> s;
	for (int i = 0; i < n - 1; i++) {
		char c;
		cin >> c;
		s.push_back(c == 'D' ? true : false);
	}

	SegTree up(n), down(n);
	up.update(0, n - 1, -1);
	down.update(0, n - 1, -1);
	if (s[0]) {
		down.update(nums[0], nums[0], 1);
	} else {
		up.update(nums[0], nums[0], 1);
	}
	for (int i = 1; i < n; i++) {
		int val = max(up.query(0, nums[i]).value, down.query(nums[i], n - 1).value) + 1;
		// up.debug();
		// down.debug();
		// cout << nums[i] << " " << val << endl;
		if (s[val]) {
			down.update(nums[i], nums[i], val + 1);
		} else {
			up.update(nums[i], nums[i], val + 1);
		}
	}
	cout << max(up.query(0, n - 1).value, down.query(0, n - 1).value) << endl;
}