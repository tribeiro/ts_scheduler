import math
import numpy

class Target(object):
    def __init__(self,
                 targetid=0,
                 fieldid=0,
                 filter="",
                 ra_rad=0.0,
                 dec_rad=0.0,
                 ang_rad=0.0,
                 num_exp=0,
                 exp_times=[]):

        self.targetid = targetid
        self.fieldid = fieldid
        self.filter = filter
        self.ra_rad = ra_rad
        self.dec_rad = dec_rad
        self.ang_rad = ang_rad
        self.num_exp = num_exp
        self.exp_times = list(exp_times)

        #conditions
        self.time = 0.0
        self.airmass = 0.0
        self.sky_brightness = 0.0
        self.cloud = 0.0
        self.seeing = 0.0

        #computed at proposal
        self.propid = 0
        self.need = 0.0
        self.bonus = 0.0
        self.value = 0.0
        #internal proposal book-keeping
        self.goal = 0
        self.visits = 0
        self.progress = 0.0
        self.groupid = 0
        self.groupix = 0

        #computed at driver
        self.alt_rad = 0.0
        self.az_rad = 0.0
        self.rot_rad = 0.0
        self.telalt_rad = 0.0
        self.telaz_rad = 0.0
        self.telrot_rad = 0.0
        self.propboost = 1.0
        self.slewtime = 0.0
        self.cost = 0.0
        self.rank = 0.0

        #assembled at driver
        self.num_props = 0
        self.propid_list = []
        self.need_list = []
        self.bonus_list = []
        self.value_list = []
        self.propboost_list = []

        #stamped at observation
        self.last_visit_time = 0.0

    def get_copy(self):

        newtarget = Target()
        newtarget.targetid = self.targetid
        newtarget.fieldid = self.fieldid
        newtarget.filter = self.filter
        newtarget.ra_rad = self.ra_rad
        newtarget.dec_rad = self.dec_rad
        newtarget.ang_rad = self.ang_rad
        newtarget.num_exp = self.num_exp
        newtarget.exp_times = list(self.exp_times)
        newtarget.time = self.time
        newtarget.airmass = self.airmass
        newtarget.sky_brightness = self.sky_brightness
        newtarget.cloud = self.cloud
        newtarget.seeing = self.seeing
        newtarget.propid = self.propid
        newtarget.need = self.need
        newtarget.bonus = self.bonus
        newtarget.value = self.value
        newtarget.goal = self.goal
        newtarget.visits = self.visits
        newtarget.progress = self.progress
        newtarget.groupid = self.groupid
        newtarget.groupix = self.groupix
        newtarget.alt_rad = self.alt_rad
        newtarget.az_rad = self.az_rad
        newtarget.rot_rad = self.rot_rad
        newtarget.telalt_rad = self.telalt_rad
        newtarget.telaz_rad = self.telaz_rad
        newtarget.telrot_rad = self.telrot_rad
        newtarget.propboost = self.propboost
        newtarget.slewtime = self.slewtime
        newtarget.cost = self.cost = 0.0
        newtarget.rank = self.rank = 0.0
        newtarget.num_props = self.num_props
        newtarget.propid_list = list(self.propid_list)
        newtarget.need_list = list(self.need_list)
        newtarget.bonus_list = list(self.bonus_list)
        newtarget.value_list = list(self.value_list)
        newtarget.propboost_list = list(self.propboost_list)

        return newtarget

    def __str__(self):
        return ("targetid=%d field=%d filter=%s exp_times=%s ra=%.3f dec=%.3f ang=%.3f "
                "alt=%.3f az=%.3f rot=%.3f "
                "telalt=%.3f telaz=%.3f telrot=%.3f "
                "time=%.1f airmass=%.3f brightness=%.3f "
                "cloud=%.2f seeing=%.2f "
                "visits=%i progress=%.2f%% "
                "groupid=%i groupix=%i "
                "need=%.3f bonus=%.3f value=%.3f propboost=%.3f "
                "propid=%s need=%s bonus=%s value=%s propboost=%s "
                "slewtime=%.3f cost=%.3f rank=%.3f" %
                (self.targetid, self.fieldid, self.filter, str(self.exp_times),
                 self.ra, self.dec, self.ang,
                 self.alt, self.az, self.rot,
                 self.telalt, self.telaz, self.telrot,
                 self.time, self.airmass, self.sky_brightness,
                 self.cloud, self.seeing,
                 self.visits, 100 * self.progress,
                 self.groupid, self.groupix,
                 self.need, self.bonus, self.value, self.propboost,
                 self.propid_list, numpy.round(self.need_list, 3), numpy.round(self.bonus_list, 3),
                 numpy.round(self.value_list, 3), numpy.round(self.propboost_list, 3),
                 self.slewtime, self.cost, self.rank))

    @property
    def ra(self):
        return math.degrees(self.ra_rad)

    @property
    def dec(self):
        return math.degrees(self.dec_rad)

    @property
    def ang(self):
        return math.degrees(self.ang_rad)

    @property
    def alt(self):
        return math.degrees(self.alt_rad)

    @property
    def az(self):
        return math.degrees(self.az_rad)

    @property
    def rot(self):
        return math.degrees(self.rot_rad)

    @property
    def telalt(self):
        return math.degrees(self.telalt_rad)

    @property
    def telaz(self):
        return math.degrees(self.telaz_rad)

    @property
    def telrot(self):
        return math.degrees(self.telrot_rad)

    @classmethod
    def from_topic(cls, topic):
        """Alternate initializer.

        Parameters
        ----------
        topic : SALPY_scheduler.targetC
            The target topic instance.

        Returns
        -------
        schedulerTarget.Target
        """
        return cls(topic.targetId, topic.fieldId, topic.filter, math.radians(topic.ra),
                   math.radians(topic.dec), math.radians(topic.angle), topic.num_exposures,
                   topic.exposure_times)
