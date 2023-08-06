from pdme.measurement import OscillatingDipole, OscillatingDipoleArrangement
import pdme
from deepdog.bayes_run import DotInput
import datetime
import numpy
from dataclasses import dataclass
import logging
from typing import Sequence, Tuple
import csv
import itertools
import multiprocessing

_logger = logging.getLogger(__name__)


def get_a_result(discretisation, dots, index):
	return (index, discretisation.solve_for_index(dots, index))


@dataclass
class SingleDipoleDiagnostic():
	model: str
	index: Tuple
	bounds: Tuple
	actual_dipole: OscillatingDipole
	result_dipole: OscillatingDipole
	success: bool

	def __post_init__(self) -> None:
		self.p_actual_x = self.actual_dipole.p[0]
		self.p_actual_y = self.actual_dipole.p[1]
		self.p_actual_z = self.actual_dipole.p[2]
		self.s_actual_x = self.actual_dipole.s[0]
		self.s_actual_y = self.actual_dipole.s[1]
		self.s_actual_z = self.actual_dipole.s[2]
		self.p_result_x = self.result_dipole.p[0]
		self.p_result_y = self.result_dipole.p[1]
		self.p_result_z = self.result_dipole.p[2]
		self.s_result_x = self.result_dipole.s[0]
		self.s_result_y = self.result_dipole.s[1]
		self.s_result_z = self.result_dipole.s[2]
		self.w_actual = self.actual_dipole.w
		self.w_result = self.result_dipole.w


class Diagnostic():
	'''
	Represents a diagnostic for a single dipole moment given a set of discretisations.

	Parameters
	----------
	dot_inputs : Sequence[DotInput]
		The dot inputs for this diagnostic.
	discretisations_with_names : Sequence[Tuple(str, pdme.model.Model)]
		The models to evaluate.
	actual_model_discretisation : pdme.model.Discretisation
		The discretisation for the model which is actually correct.
	filename_slug : str
		The filename slug to include.
	run_count: int
		The number of runs to do.
	'''
	def __init__(self, actual_dipole_moment: numpy.ndarray, actual_dipole_position: numpy.ndarray, actual_dipole_frequency: float, dot_inputs: Sequence[DotInput], discretisations_with_names: Sequence[Tuple[str, pdme.model.Discretisation]], filename_slug: str) -> None:
		self.dipoles = OscillatingDipoleArrangement([OscillatingDipole(actual_dipole_moment, actual_dipole_position, actual_dipole_frequency)])
		self.dots = self.dipoles.get_dot_measurements(dot_inputs)

		self.discretisations_with_names = discretisations_with_names
		self.model_count = len(self.discretisations_with_names)

		self.csv_fields = ["model", "index", "bounds", "p_actual_x", "p_actual_y", "p_actual_z", "s_actual_x", "s_actual_y", "s_actual_z", "w_actual", "success", "p_result_x", "p_result_y", "p_result_z", "s_result_x", "s_result_y", "s_result_z", "w_result"]

		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		self.filename = f"{timestamp}-{filename_slug}.diag.csv"

	def go(self):
		with open(self.filename, "a", newline="") as outfile:
			# csv fields
			writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect='unix')
			writer.writeheader()

		for (name, discretisation) in self.discretisations_with_names:
			_logger.info(f"Working on discretisation {name}")

			results = []
			with multiprocessing.Pool(multiprocessing.cpu_count() - 1 or 1) as pool:
				results = pool.starmap(get_a_result, zip(itertools.repeat(discretisation), itertools.repeat(self.dots), discretisation.all_indices()))

			with open(self.filename, "a", newline='') as outfile:
				writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect='unix', extrasaction="ignore")

				for idx, result in results:

					bounds = discretisation.bounds(idx)

					actual_success = result.success and result.cost <= 1e-10
					diag_row = SingleDipoleDiagnostic(name, idx, bounds, self.dipoles.dipoles[0], discretisation.model.solution_as_dipoles(result.normalised_x)[0], actual_success)
					row = vars(diag_row)
					_logger.debug(f"Writing result {row}")
					writer.writerow(row)
