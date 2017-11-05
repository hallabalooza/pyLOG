# pyLOG
# Copyright (C) 2017  Hallabalooza
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# <http://www.gnu.org/licenses/>.

########################################################################################################################
########################################################################################################################
########################################################################################################################

import datetime
import logging
import os, os.path

########################################################################################################################
########################################################################################################################
########################################################################################################################

class RotatingFileHandler(logging.handlers.BaseRotatingHandler):
  """
  @brief  Handler for logging to a file, rotating the log file at certain time intervals.
  """

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, interval="month", fdoweek="Mo", location=".", naming="%Y%m%d_%W_%H%M%S.log", collector="current.log"):
    """
    @brief  constructor
    @param  interval    The interval a desired log file shall contain. Shall be one of {second, minute, hour, day, week, month, year}.
    @param  fdoweek     The first day of week. Shall be one of {Mo, Su}.
    @param  location    The location where the log files shall be stored.
    @param  naming      The 'datetime.strftime' format string the log files shall be named according to.
    @param  collector   A unique identifier of the file in location where data is collected.
    """
    if ( interval not in ["second", "minute", "hour", "day", "week", "month", "year"] ):
      raise ValueError("Wrong 'interval' parameter. Expected is a value of {second, minute, hour, day, week, month, year}.")
    if ( fdoweek not in ["Mo", "Su"] ):
      raise ValueError("Wrong 'fdoweek' parameter. Expected is a value of {Mo, Su}.")

    self.__interval         = interval
    self.__fdoweek          = fdoweek
    self.__location         = location
    self.__naming           = naming
    self.__source           = os.path.normpath(os.path.join(self.__location, "{}".format(collector)))
    self.__fdoweekdirective = {"Mo":"%W", "Su":"%U"}[self.__fdoweek]
    self.__stamplast        = datetime.datetime.now()
    self.__stampnaming      = None

    if ( False == os.path.exists(os.path.dirname(self.__source)) ):
      os.makedirs(os.path.dirname(self.__source))

    logging.handlers.BaseRotatingHandler.__init__(self, self.__source, "a", encoding=None, delay=False)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def doRollover(self):
    """
    @brief  Do a rollover if a new interval starts.
    """
    if ( self.stream ):
      self.stream.close()
      self.stream = None
      dst = os.path.normpath(os.path.join(self.__location, self.__stampnaming.strftime(self.__naming)))
      if ( os.path.exists(self.__source) ):
        if ( os.path.exists(dst) ):
          os.remove(dst)
        os.rename(self.__source, dst)
      else:
        raise ValueError("Source does not exist")

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def shouldRollover(self, record):
    """
    @brief  Determine if the supplied record would cause a rollover.
    @param  record  The data structure containing all informations respective to the current event.
    @return A boolean information whether a rollover shall be processed.
    """
    self.__stampnaming = None
    now                = datetime.datetime.fromtimestamp(record.created)
    weeknr_now         = int(             now.strftime(self.__fdoweekdirective))
    weeknr_last        = int(self.__stamplast.strftime(self.__fdoweekdirective))

    if ( (self.__interval == "second" and self.__stamplast.second < now.second) or
         (self.__interval == "minute" and self.__stamplast.minute < now.minute) or
         (self.__interval == "hour"   and self.__stamplast.hour   < now.hour  ) or
         (self.__interval == "day"    and self.__stamplast.day    < now.day   ) or
         (self.__interval == "week"   and weeknr_last             < weeknr_now) or
         (self.__interval == "month"  and self.__stamplast.month  < now.month ) or
         (self.__interval == "year"   and self.__stamplast.year   < now.year  )
       ):
      if   ( self.__interval == "second" ): pass
      elif ( self.__interval == "minute" ): self.__stampnaming = self.__stamplast.replace(second=0)
      elif ( self.__interval == "hour"   ): self.__stampnaming = self.__stamplast.replace(second=0, minute=0)
      elif ( self.__interval == "day"    ): self.__stampnaming = self.__stamplast.replace(second=0, minute=0, hour=0)
      elif ( self.__interval == "week"   ): self.__stampnaming = self.__stamplast.replace(second=0, minute=0, hour=0)
      elif ( self.__interval == "month"  ): self.__stampnaming = self.__stamplast.replace(second=0, minute=0, hour=0, day=0)
      elif ( self.__interval == "year"   ): self.__stampnaming = self.__stamplast.replace(second=0, minute=0, hour=0, day=0, month=0)
      self.__stamplast = now
      return 1
    else:
      return 0

########################################################################################################################
########################################################################################################################
########################################################################################################################

if ( __name__ == '__main__' ):
  pass
