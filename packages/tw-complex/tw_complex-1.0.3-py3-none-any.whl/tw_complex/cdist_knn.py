from math import floor
from typing import List, Literal, Tuple

import numpy as np
from scipy.spatial.distance import cdist
from sklearn.neighbors import KNeighborsClassifier


class CDistAndKNN:
    """
    This algorithm first counts the exact result for the part of ally_villages
    using `cdist` and then with `KNN model` with `N=3` tries to predict the rest,
    see `result` method.

    NOTES
    -----
    With `precision=1` and `_max_ally`, `_max_enemy` equals to something
    very big like `10**10`, it is the brute force.
    """

    def __init__(
        self,
        ally_villages: np.ndarray,
        enemy_villages: np.ndarray,
        min_radius: float,
        max_radius: float,
        _precision: float = 0.8,
        _max_ally: int = 5000,
        _max_enemy: int = 20000,
    ) -> None:
        self.all_ally = ally_villages
        self.all_enemy = enemy_villages
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.precision = _precision
        self.max_ally = _max_ally
        self.max_enemy = _max_enemy
        self.neighbors = 3

    def result(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Method is used to run algorithm.

        Returns
        -------
        Tuple of np.ndarray is returned:

        (below `x` is minimum of distances to every enemy village)

        `front_lst` : array with coords `x <= min_radius`

        `back_lst` : array with coords `min_radius < x < max_radius`

        NOTES
        -----
        - Step 1: Take some part of the ally_villages and calculate `X_TRAIN` with
        precise status calculated
        - Step 2: Create KNN model based on `X_TRAIN` data
        - Step 3: Predict the rest of ally_villages with given model
        - Step 4: Return front and back villages, we do not care much about very far ones
        """
        LENGTH: int = self.all_ally.size
        LENGTH = min(max(1000, floor(self.precision * (LENGTH / 2))), self.max_ally)

        X_TRAIN: np.ndarray = self.all_ally[:LENGTH]
        X_PREDICT: np.ndarray = self.all_ally[LENGTH:]

        X_TRAIN, Y_TRAIN = self.use_cdist(
            ally_villages=X_TRAIN,
            enemy_villages=self.all_enemy[
                : min(
                    max(0.4, floor(self.all_enemy.size * self.precision)),
                    self.max_enemy,
                )
            ],
            min_radius=self.min_radius,
            max_radius=self.max_radius,
        )
        if X_PREDICT.size > 0:
            K = self.neighbors
            model = KNeighborsClassifier(n_neighbors=K)
            model.fit(X_TRAIN, Y_TRAIN)
            Y_KNN_PREDICTED = model.predict(X_PREDICT)
        else:
            Y_KNN_PREDICTED = np.array([])

        front_lst: List[np.ndarray] = []
        back_lst: List[np.ndarray] = []

        np_coords: np.ndarray
        status: Literal[0, 1, 2]
        for np_coords, status in zip(
            self.all_ally, np.append(Y_TRAIN, Y_KNN_PREDICTED)
        ):
            if status == 0:
                front_lst.append(np_coords)
            elif status == 1:
                back_lst.append(np_coords)
        return np.array(front_lst), np.array(back_lst)

    def use_cdist(
        self,
        ally_villages: np.ndarray,
        enemy_villages: np.ndarray,
        min_radius: float,
        max_radius: float,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Adds precise states to given ally_villages, calculating all possible distances
        to enemy_villages using `cdist`

        Returns
        -------
        Tuple of np.ndarray is returned:

        `lst` : array with coords

        `status` : array with three diffrent statuses where `x` is minimum of distances:

            - `0` when village is close to enemy, `x <= min_radius`
            - `1` when village is in welcome position, `min_radius < x < max_radius`
            - `2` when village is too far from enemy, `x >= max_radius`
        """

        lst: List[np.ndarray] = list()
        status: List[Literal[0, 1, 2]] = list()

        # We use sq of distance
        C = cdist(ally_villages, enemy_villages, "sqeuclidean")
        sq_min_radius: float = min_radius**2
        sq_max_radius: float = max_radius**2

        for point, i in zip(ally_villages, C):
            x: np.float64 = np.amin(i)
            lst.append(point)
            if x <= sq_min_radius:
                status.append(0)
            elif x >= sq_max_radius:
                status.append(2)
            else:
                status.append(1)

        return (
            np.array(lst),
            np.array(status),
        )
