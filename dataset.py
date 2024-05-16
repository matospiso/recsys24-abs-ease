from copy import deepcopy
import numpy as np
import scipy.sparse as sp

np.random.seed(12345)


class UserSessionItemDataset:
    def __init__(self, train, val, test, n_user_sessions, n_items):
        """
        expect train, val, test with three columns: ["user_session_id", "item_id", "rating"]
        """
        self._train = train
        self._val = val
        self._test = test
        self.n_user_sessions = n_user_sessions
        self.n_items = n_items

    @property
    def train(self):
        return deepcopy(self._train)

    @property
    def val(self):
        return deepcopy(self._val)

    @property
    def test(self):
        return deepcopy(self._test)


def get_train_test_matrices(dataset: UserSessionItemDataset, split, target_ratio: float):
    train_df = dataset.train  # train only on training interactions
    # test on the selected split
    if split == "val":
        test_df = dataset.val
    elif split == "test":
        test_df = dataset.test
    else:
        raise ValueError(f"unknown split {split}") 
    
    # PREPARE TEST SPLIT
    # use positive and negative ratings
    # map test user sessions to 0...k and save their count
    test_user_session_count = test_df.user_session_id.nunique()
    test_user_session_to_idx = {
        us: idx for idx, us in enumerate(test_df.user_session_id.unique())
    }
    test_df["user_session_id"] = test_df["user_session_id"].map(test_user_session_to_idx)
    test_df["target"] = False
    # select target_ratio of positive interactions as targets
    #    and target_ratio of negative interactions as targets
    for us in range(test_user_session_count):
        # positive part
        us_pos_part = test_df[(test_df.user_session_id == us) & (test_df.rating == 1.)]
        target_size = round(len(us_pos_part)*target_ratio)
        target_indices = np.random.choice(np.arange(len(us_pos_part)), target_size, replace=False)
        target_values = np.zeros(len(us_pos_part), dtype=bool)
        target_values[target_indices] = True
        test_df.loc[(test_df.user_session_id == us) & (test_df.rating == 1.), "target"] = target_values
        # negative part
        us_neg_part = test_df[(test_df.user_session_id == us) & (test_df.rating == -1.)]
        target_size = round(len(us_neg_part)*target_ratio)
        target_indices = np.random.choice(np.arange(len(us_neg_part)), target_size, replace=False)
        target_values = np.zeros(len(us_neg_part), dtype=bool)
        target_values[target_indices] = True
        test_df.loc[(test_df.user_session_id == us) & (test_df.rating == -1.), "target"] = target_values

    # create training CSR matrix
    n_user_sessions = dataset.n_user_sessions
    n_items = dataset.n_items
    train_X = sp.csr_matrix((train_df.rating, (train_df.user_session_id, train_df.item_id)), shape=(n_user_sessions, n_items))
    # we could compress the first dimension (to ignore 0 rows), but it doesn't affect anything and this is easier

    # create test input CSR matrix
    input_df = test_df[~test_df.target]
    test_X = sp.csr_matrix((input_df.rating, (input_df.user_session_id, input_df.item_id)), shape=(test_user_session_count, n_items))

    # create positive only input CSR matrix
    test_X_pos = deepcopy(test_X)
    test_X_pos.data *= test_X_pos.data == 1.
    test_X_pos.eliminate_zeros()

    # create test_targets CSR matrix
    target_df = test_df[test_df.target]
    test_y = sp.csr_matrix((target_df.rating, (target_df.user_session_id, target_df.item_id)), shape=(test_user_session_count, n_items))

    return train_X, test_X_pos, test_X, test_y