from dataclasses import dataclass
from typing import Union, List, Optional

import numpy

from .critical_region import CriticalRegion
from .geometry.polytope_operations import get_chebyshev_information
from .mplp_program import MPLP_Program
from .mpqp_program import MPQP_Program
from .utils.general_utils import make_column


@dataclass
class Solution:
    """The Solution object is the output of multiparametric solvers, it contains all of the critical regions as well as holds a copy of the original problem that was solved"""
    program: Union[MPLP_Program, MPQP_Program]
    critical_regions: List[CriticalRegion]

    def add_region(self, region: CriticalRegion) -> None:
        """
        Adds a region to the solution

        :param region: region to add to the solution
        :return: None
        """
        self.critical_regions.append(region)

    def evaluate(self, theta_point: numpy.ndarray) -> Optional[numpy.ndarray]:
        """
        returns the optimal x* from the solution

        :param theta_point: an uncertainty realization
        :return: the calculated x* from theta
        """

        for region in self.critical_regions:
            if region.is_inside(theta_point):
                return region.evaluate(theta_point)
        return None

    def get_region(self, theta_point: numpy.ndarray) -> Optional[CriticalRegion]:
        """
        Find the critical region in the solution that corresponds to the theta provided

        :param theta_point: an uncertainty realization
        :return: the region that contains theta
        """
        for region in self.critical_regions:
            if region.is_inside(theta_point):
                return region
        return None

    def verify_solution(self) -> bool:
        """
        This can be called to verify that all of the critical regions agree with the optimization problem. With problems
        with numerically small critical regions the deterministic optimizer value could fail. This does NOT necessarily
        mean that the critical region is at fault but that perhaps more analysis should be done. This is especially
        apparent with critical regions with chebychev radii on the order of sqrt(machine epsilon).

        :return: True if all is verified, else False
        """

        print(len(self.critical_regions))

        for region in self.critical_regions:
            sol = get_chebyshev_information(region)
            theta = make_column(sol.sol)[0:numpy.size(sol.sol) - 1]

            x_star = region.evaluate(theta)
            l_star = region.lagrange_multipliers(theta)
            active_set = region.active_set

            soln = self.program.solve_theta(theta)

            if not numpy.allclose(soln.sol, x_star.flatten()):
                return False
            if not numpy.allclose(soln.dual[soln.active_set], -l_star.flatten()):
                return False
            if numpy.allclose(soln.active_set, active_set):
                return False

        return True

    def verify_theta(self, theta_point: numpy.ndarray) -> bool:
        """
        Checks that the result of the solution is consistent with theta substituted multiparametric problem

        :param theta_point: an uncertainty realization
        :return: True if they are the same, False if they are different
        """
        region = self.get_region(theta_point)

        x_star = region.evaluate(theta_point)
        l_star = region.lagrange_multipliers(theta_point)
        r_active_set = region.active_set

        soln = self.program.solve_theta(theta_point)

        if numpy.allclose(soln.sol, x_star.flatten()):
            if numpy.allclose(soln.dual[soln.active_set], -l_star.flatten()):
                if numpy.allclose(soln.active_set, r_active_set):
                    return True

        return False

    def theta_dim(self) -> int:
        return self.program.num_t()

    def evaluate_objective(self, theta_point) -> Optional[numpy.ndarray]:
        """
        Given a realization of an uncertainty parameter, calculate the objective value

        :param theta_point:
        :return:
        """
        x_star = self.evaluate(theta_point)
        if x_star is not None:
            return self.program.evaluate_objective(x_star, theta_point)
        return None
