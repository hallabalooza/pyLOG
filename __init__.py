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

import enum
import inspect
import logging, logging.config

########################################################################################################################
########################################################################################################################
########################################################################################################################

class LogLvl(enum.IntEnum):
  """
  @brief  The logging level symbolic identifiers.
  """

  CRITICAL = 50
  ERROR    = 40
  WARNING  = 30
  INFO     = 20
  DEBUG    = 10
  NOTSET   =  0

########################################################################################################################
########################################################################################################################
########################################################################################################################

def LogInit(cfg):
  """
  @brief  The logging initialization function.
  @param  cfg  A logging.config data structure.
  """
  logging.config.dictConfig(cfg)

########################################################################################################################
########################################################################################################################
########################################################################################################################

class Log(object):
  """
  @brief  The logging class.
  """

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def __init__(self, log):
    """
    @brief  Constructor.
    @param  log  A logging.config.loggers name.
    @param  lvl  A LogLvl.
    """
    self.__log = logging.getLogger(log)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def log(self, lvl, msg, *args, **kwargs):
    """
    @brief  Logs a message 'msg' with level 'lvl' on this logger.
    @param  lvl     See https://docs.python.org/3/library/logging.html => Logger.log(lvl, msg, *args, **kwargs)
    @param  msg     See https://docs.python.org/3/library/logging.html => Logger.log(lvl, msg, *args, **kwargs)
    @param  args    See https://docs.python.org/3/library/logging.html => Logger.log(lvl, msg, *args, **kwargs)
    @param  kwargs  See https://docs.python.org/3/library/logging.html => Logger.log(lvl, msg, *args, **kwargs)
    """
    if ( None != self.__log ):
      self.__log.log(lvl.value, msg, *args, **kwargs)

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def log_callinfo(self):
    """
    @brief  Logs a message 'msg' with level 'DEBUG' on this logger, containing call informations.
    """
    if ( None != self.__log ):
      self.__log.log(LogLvl.DEBUG, "CALL: {}/{}".format(inspect.stack()[1].frame.f_locals["self"].__class__.__name__,
                                                        inspect.stack()[1].function
                                                       )
                    )

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  @property
  def loglvl(self):
    """
    @brief  Get the currecntly active logging level.
    """
    return self.__log.getEffectiveLevel()

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  @loglvl.setter
  def loglvl(self, lvl):
    """
    @brief  Set the logging level.
    """
    self.__log.setLevel(lvl)

########################################################################################################################
########################################################################################################################
########################################################################################################################

if ( __name__ == '__main__' ):
  pass
