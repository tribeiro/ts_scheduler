import numpy
import unittest
import warnings

from ts_scheduler.sky_model import AstronomicalSkyModel

from tests.test_constants import LSST_SITE, LSST_START_TIMESTAMP

class AstronomicalSkyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings('ignore', category=RuntimeWarning, append=True)
        warnings.filterwarnings('ignore', category=FutureWarning, append=True)
        cls.astro_sky = AstronomicalSkyModel(LSST_SITE)
        cls.time_tolerance = 1e-6
        cls.sun_altitude = -12.0

    def create_ra_dec(self):
        self.ra_rads = numpy.radians(numpy.linspace(0., 90., 19))
        self.dec_rads = numpy.radians(numpy.linspace(-90., 0., 19))

    def check_night_boundary_tuple(self, truth_set_timestamp, truth_rise_timestamp):
        (set_timestamp, rise_timestamp) = self.astro_sky.get_night_boundaries(self.sun_altitude)
        self.assertAlmostEqual(set_timestamp, truth_set_timestamp, delta=self.time_tolerance)
        self.assertAlmostEqual(rise_timestamp, truth_rise_timestamp, delta=self.time_tolerance)

    def test_basic_information_after_initial_creation(self):
        self.assertIsNotNone(self.astro_sky.date_profile)
        self.assertEqual(self.astro_sky.date_profile.timestamp, 0)
        self.assertIsNotNone(self.astro_sky.sky_brightness)
        self.assertIsNotNone(self.astro_sky.sun)

    def test_update_mechanism(self):
        self.astro_sky.update(LSST_START_TIMESTAMP)
        self.assertEqual(self.astro_sky.date_profile.timestamp, LSST_START_TIMESTAMP)

    def test_sky_brightness_retrieval_internal_time_array_of_positions(self):
        self.create_ra_dec()
        self.astro_sky.update(LSST_START_TIMESTAMP)
        sky_mags = self.astro_sky.get_sky_brightness(self.ra_rads, self.dec_rads)
        self.assertEqual(len(sky_mags), 6)
        self.assertEqual(sky_mags['g'].size, self.ra_rads.size)

    def test_sky_brightness_retrieval_from_timestamp_set_and_array_of_positions(self):
        initial_timestamp = 1641081600.
        time_step = 5.0 * 60.0
        number_of_steps = 10
        self.create_ra_dec()
        sky_mags = self.astro_sky.get_sky_brightness_timeblock(initial_timestamp, time_step,
                                                               number_of_steps,
                                                               self.ra_rads, self.dec_rads)
        self.assertEqual(len(sky_mags), number_of_steps)
        self.assertEqual(sky_mags[0]['g'].size, self.ra_rads.size)
        self.assertAlmostEqual(sky_mags[0]['u'][0], 22.62361215, delta=1e-7)
        self.assertAlmostEqual(sky_mags[0]['g'][0], 21.92863773, delta=1e-7)
        self.assertAlmostEqual(sky_mags[0]['r'][0], 20.80615409, delta=1e-7)
        self.assertAlmostEqual(sky_mags[0]['i'][0], 19.79378908, delta=1e-7)
        self.assertAlmostEqual(sky_mags[0]['z'][0], 18.78361422, delta=1e-7)
        self.assertAlmostEqual(sky_mags[0]['y'][0], 17.56788428, delta=1e-7)

    def test_get_night_boundaries(self):
        # 2022/01/01
        # At sunset
        self.astro_sky.update(1641084532.843324)
        self.check_night_boundary_tuple(1641084532.843324, 1641113113.755558)
        # In night
        self.astro_sky.update(1641098823.29944)
        self.check_night_boundary_tuple(1641084532.843324, 1641113113.755558)
        # At sunrise, next night bounds
        self.astro_sky.update(1641113113.755558)
        self.check_night_boundary_tuple(1641170940.8965435, 1641199562.951024)
        # In daytime, next night bounds
        self.astro_sky.update(1641113114.755558)
        self.check_night_boundary_tuple(1641170940.8965435, 1641199562.951024)
        self.astro_sky.update(1641133114.755558)
        self.check_night_boundary_tuple(1641170940.8965435, 1641199562.951024)
        # 2022/02/01
        self.astro_sky.update(1643762299.348505)
        self.check_night_boundary_tuple(1643762299.348505, 1643793352.557206)
        # 2022/03/08
        self.astro_sky.update(1646784061.294245)
        self.check_night_boundary_tuple(1646784061.294245, 1646819228.784648)
        # 2022/07/02
        # At sunset
        self.astro_sky.update(1656802219.515093)
        self.check_night_boundary_tuple(1656802219.515093, 1656845034.696892)
        # At sunrise, next night bounds
        self.astro_sky.update(1656845034.696892)
        self.check_night_boundary_tuple(1656888641.725961, 1656931433.3882337)
        # In daytime, next night bounds
        self.astro_sky.update(1656845035.696892)
        self.check_night_boundary_tuple(1656888641.725961, 1656931433.3882337)
        # 2022/10/17
        self.astro_sky.update(1666050479.261601)
        self.check_night_boundary_tuple(1666050479.261601, 1666084046.869362)
        # 2025/04/01
        self.astro_sky.update(1743550264.401366)
        self.check_night_boundary_tuple(1743550264.401366, 1743588178.165652)
        # 2027/06/21
        self.astro_sky.update(1813618020.702736)
        self.check_night_boundary_tuple(1813618020.702736, 1813660969.989451)
        # 2031/09/20
        self.astro_sky.update(1947713387.331446)
        self.check_night_boundary_tuple(1947713387.331446, 1947750106.804758)

    def test_moon_separation_function(self):
        initial_timestamp = 1641081600 + (.04166666666 * 3600 * 24)
        self.create_ra_dec()
        self.astro_sky.update(initial_timestamp)
        self.astro_sky.get_sky_brightness(self.ra_rads, self.dec_rads)
        field_moon_sep = self.astro_sky.get_moon_separation(self.ra_rads, self.dec_rads)
        self.assertEqual(field_moon_sep.size, 19)
        self.assertAlmostEqual(field_moon_sep[0], numpy.radians(64.69897587))

    def test_moon_sun_information(self):
        initial_timestamp = 1641081600 + (.04166666666 * 3600 * 24)
        self.create_ra_dec()
        self.astro_sky.update(initial_timestamp)
        self.astro_sky.get_sky_brightness(self.ra_rads, self.dec_rads)
        info = self.astro_sky.get_moon_sun_info(0.61086524, -0.78539816)
        self.assertEqual(len(info), 11)
        self.assertAlmostEqual(info["moonPhase"], 0.8692556023597717, delta=1e-7)
        self.assertAlmostEqual(info["moonDist"], 1.6289850022, delta=1e-7)
        self.assertAlmostEqual(info["moonDec"], -0.4415861752238436, delta=1e-7)
        self.assertAlmostEqual(info["moonRA"], 4.72440671517994, delta=1e-7)

    def test_target_information(self):
        initial_timestamp = 1641081600 + (.04166666666 * 3600 * 24)
        self.create_ra_dec()
        self.astro_sky.update(initial_timestamp)
        self.astro_sky.get_sky_brightness(self.ra_rads, self.dec_rads)
        info = self.astro_sky.get_target_information()
        self.assertEqual(len(info), 3)
        self.assertEqual(info['airmass'].size, self.ra_rads.size)
        self.assertEqual(info['alts'].size, self.ra_rads.size)
        self.assertEqual(info['azs'].size, self.ra_rads.size)
        self.assertAlmostEqual(info['airmass'][0], 1.9853499253850075, delta=1e-7)
        self.assertAlmostEqual(info['alts'][0], 0.52786436029017303, delta=1e-7)
        self.assertTrue(numpy.isnan(info['azs'][0]))
