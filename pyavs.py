# AvsP - an AviSynth editor
#
# GPo mod based on the last release from vdcrim (2.5.1)
# Modifications by pinterf (pfmod)
#
# Copyright 2007 Peter Jang <http://www.avisynth.org/qwerpoi>
#           2010-2017 the AvsPmod authors <https://github.com/avspmod/avspmod>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA, or visit
#  http://www.gnu.org/copyleft/gpl.html .

# pyavs - AVI functions via AviSynth in Python
# Drawing uses VFW on Windows and generical wxPython support on other platforms
#
# Dependencies:
#     Python (tested on v2.6 and v2.7)
#     wxPython (for *nix, tested on v2.8 and v2.9)
#     cffi and its dependencies (only for x86-64, tested on v0.9.2)
#         pycparser
#         Visual C++
#     avisynth_c.h (only for x86-64, interface 5, or at least 3 + colorspaces
#                   from 5, tested with the header used by x264)
# Scripts:
#     avisynth.py (Python AviSynth/AvxSynth wrapper, only for x86-32)
#     avisynth_cffi.py (Python AviSynth wrapper, only for x86-64)

import sys
import os
import ctypes
import re
import func
import struct
import utils

x86_64 = sys.maxsize > 2**32
if x86_64:
    import avisynth_cffi as avisynth
else:
    import avisynth
import global_vars
import threading
#import time

try: _
except NameError:
    def _(s): return s

"""
def avs_plus_get_colorspace_name(pixel_type):

    avs_ColorspaceDict = {
    	avs_plus.CS_BGR24: "RGB24",
    	avs_plus.CS_BGR32: "RGB32",
    	avs_plus.CS_YUY2 : "YUY2",
    	avs_plus.CS_YV24 : "YV24",
    	avs_plus.CS_YV16 : "YV16",
    	avs_plus.CS_YV12 : "YV12",
    	avs_plus.CS_I420 : "YV12",
    	avs_plus.CS_YUV9 : "YUV9",
    	avs_plus.CS_YV411: "YV411",
    	avs_plus.CS_Y8   : "Y8",
    	avs_plus.CS_YUV420P10: "YUV420P10",
    	avs_plus.CS_YUV422P10: "YUV422P10",
    	avs_plus.CS_YUV444P10: "YUV444P10",
    	avs_plus.CS_Y10      : "Y10",
    	avs_plus.CS_YUV420P12: "YUV420P12",
    	avs_plus.CS_YUV422P12: "YUV422P12",
    	avs_plus.CS_YUV444P12: "YUV444P12",
    	avs_plus.CS_Y12      : "Y12",
    	avs_plus.CS_YUV420P14: "YUV420P14",
    	avs_plus.CS_YUV422P14: "YUV422P14",
    	avs_plus.CS_YUV444P14: "YUV444P14",
    	avs_plus.CS_Y14      : "Y14",
    	avs_plus.CS_YUV420P16: "YUV420P16",
    	avs_plus.CS_YUV422P16: "YUV422P16",
    	avs_plus.CS_YUV444P16: "YUV444P16",
    	avs_plus.CS_Y16      : "Y16",
    	avs_plus.CS_YUV420PS : "YUV420PS",
    	avs_plus.CS_YUV422PS : "YUV422PS",
    	avs_plus.CS_YUV444PS : "YUV444PS",
    	avs_plus.CS_Y32      : "Y32",
    	avs_plus.CS_BGR48    : "RGB48",
    	avs_plus.CS_BGR64    : "RGB64",
    	avs_plus.CS_RGBP     : "RGBP",
    	avs_plus.CS_RGBP10   : "RGBP10",
    	avs_plus.CS_RGBP12   : "RGBP12",
    	avs_plus.CS_RGBP14   : "RGBP14",
    	avs_plus.CS_RGBP16   : "RGBP16",
    	avs_plus.CS_RGBPS    : "RGBPS",
    	avs_plus.CS_YUVA420  : "YUVA420",
    	avs_plus.CS_YUVA422  : "YUVA422",
    	avs_plus.CS_YUVA444  : "YUVA444",
    	avs_plus.CS_YUVA420P10: "YUVA420P10",
    	avs_plus.CS_YUVA422P10: "YUVA422P10",
    	avs_plus.CS_YUVA444P10: "YUVA444P10",
    	avs_plus.CS_YUVA420P12: "YUVA420P12",
    	avs_plus.CS_YUVA422P12: "YUVA422P12",
    	avs_plus.CS_YUVA444P12: "YUVA444P12",
    	avs_plus.CS_YUVA420P14: "YUVA420P14",
    	avs_plus.CS_YUVA422P14: "YUVA422P14",
    	avs_plus.CS_YUVA444P14: "YUVA444P14",
    	avs_plus.CS_YUVA420P16: "YUVA420P16",
    	avs_plus.CS_YUVA422P16: "YUVA422P16",
    	avs_plus.CS_YUVA444P16: "YUVA444P16",
    	avs_plus.CS_YUVA420PS : "YUVA420PS",
    	avs_plus.CS_YUVA422PS : "YUVA422PS",
    	avs_plus.CS_YUVA444PS : "YUVA444PS",
    	avs_plus.CS_RGBAP     : "RGBAP",
    	avs_plus.CS_RGBAP10   : "RGBAP10",
    	avs_plus.CS_RGBAP12   : "RGBAP12",
    	avs_plus.CS_RGBAP14   : "RGBAP14",
    	avs_plus.CS_RGBAP16   : "RGBAP16",
    	avs_plus.CS_RGBAPS    : "RGBAPS"
    }

    if pixel_type in avs_ColorspaceDict:
        return avs_ColorspaceDict[pixel_type]
    return ''
"""

# for e.g. analysis pass
class AvsSimpleClipBase:
    def __init__(self,  script, filename='', workdir=''):
        self.initialized = False
        self.env = None
        self.clip = None
        self.error_message = None
        try:
            env = avisynth.AVS_ScriptEnvironment(6)
        except OSError: # only on OSError
            return
        except:
            self.error_message = 'At least Avisynth version 6 is required'
            return
        self.env = env

        scriptdirname, scriptbasename = os.path.split(filename)
        curdir = os.getcwdu()
        workdir = os.path.isdir(workdir) and workdir or scriptdirname
        if os.path.isdir(workdir):
            self.env.set_working_dir(workdir)
        self.env.set_global_var("$ScriptFile$", scriptbasename)
        self.env.set_global_var("$ScriptName$", filename)
        self.env.set_global_var("$ScriptDir$", scriptdirname + os.path.sep)

        try:
            self.clip = self.env.invoke('Eval', [script, filename])
            if not isinstance(self.clip, avisynth.AVS_Clip):
                err = self.env.get_error()
                self.error_message = err or 'Not a clip'
                self.env = None
                return
        except:
            err = self.env.get_error()
            self.error_message = err or 'Unknown error'
            self.clip = None
            self.env = None
            return
        finally:
            os.chdir(curdir)

        self.vi = self.clip.get_video_info()
        if not self.vi.has_video():
            self.error_message = 'Clip has no video'
            self.clip = None
            self.env = None
            return

        self.Framecount = self.vi.num_frames
        #self.current_frame = -1
        #self.scr_frame = None
        self.initialized = True
    """ not needed
    def _GetFrame(self, frame):
        if self.initialized:
            if self.current_frame == frame:
                return True
            if frame < 0:
                frame = 0
            if frame >= self.Framecount:
                frame = self.Framecount - 1
                if self.current_frame == frame:
                    return True
            self.src_frame = self.clip.get_frame(frame)
            self.current_frame = frame
            return True
        return False
    """
    def __del__(self):
        #self.src_frame = None
        self.clip = None
        self.env = None
        self.initialized = False

class AvsClipBase:

    def __init__(self,  script, filename='', workdir='', env=None, fitHeight=None,
                 fitWidth=None, oldFramecount=240, display_clip=True, reorder_rgb=False,
                 matrix=['auto', 'tv'], interlaced=False, swapuv=False, bit_depth=None,
                 callBack=None, readmatrix=None, displayFilter=None, readFrameProps=False,
                 resizeFilter=None, app=None):

        def CheckVersion(env):
            try:
                if env.check_version(9): self.avisynth_version = 9
            except: pass
            if self.avisynth_version is None:
                try:
                    if env.check_version(8): self.avisynth_version = 8
                except: pass
            if self.avisynth_version is None:
                try:
                    if env.check_version(6): self.avisynth_version = 6
                except: pass
            if self.avisynth_version is None:
                self.error_message = 'At least Avisynth version 6 is required'
                return
            return True
        # Internal variables
        self.initialized = False
        self.env = None
        self.app = app
        self.callBack = callBack
        self.name = filename
        self.error_message = None
        self.current_frame = -1
        self.pBits = None
        self.display_clip = None
        self.preview_filter = None
        self.ptrY = self.ptrU = self.ptrV = self.ptrA = None
        # Avisynth script properties
        self.Width = -1
        self.Height = -1
        self.WidthSubsampling = -1
        self.HeightSubsampling = -1
        self.Framecount = -1
        self.Framerate = -1.0
        self.FramerateNumerator = -1
        self.FramerateDenominator = -1
        self.Audiorate = -1.0
        self.Audiolength = -1
        self.Audiochannels = -1
        self.Audiobits = -1
        self.IsAudioFloat = None
        self.IsAudioInt = None
        self.IsRGB = None
        self.IsRGB24 = None
        self.IsRGB32 = None
        self.IsRGB48 = None
        self.IsRGB64 = None
        self.IsYUV = None
        self.IsYUVA = None
        self.IsYUY2 = None
        self.IsYV24 = None
        self.IsYV16 = None
        self.IsYV12 = None
        self.IsYV411 = None
        self.IsY8 = None
        self.IsY = None
        self.bits_per_component = None
        self.component_size = None
        self.num_components = None
        self.IsPlanar = None
        self.IsPlanarRGBA = None
        self.IsInterleaved = None
        self.IsFieldBased = None
        self.IsFrameBased = None
        self.GetParity  = None
        self.HasAudio = None
        self.HasVideo = None
        self.IsRGBA = None
        self.Colorspace = None
        self.sourceMatrix = '..'
        self.matrix_found = None
        self.matrix = 'Rec709'
        self.swapuv = swapuv
        self.readmatrix = readmatrix
        self.avisynth_version = None
        self.displayFilter = displayFilter
        self.resizeFilter = resizeFilter
        self.properties = ''
        self.convert_to_rgb_error = None
        self.split_clip = None
        self.IsSplitClip = None

        # Create the Avisynth script clip
        if env is not None:
            if not isinstance(env, avisynth.AVS_ScriptEnvironment):
                raise TypeError("env must be a PIScriptEnvironment or None")
        else:
            if isinstance(script, avisynth.AVS_Clip):
                raise ValueError("env must be defined when providing a clip")
            try:
                env = avisynth.AVS_ScriptEnvironment(6)
            except OSError: # only on OSError
                return
            except:
                self.error_message = 'At least Avisynth version 6 is required'
                return

        if not CheckVersion(env):
            return

        # Set frameProps reading. do not set it manuelly !!!!
        self.can_read_avisynth_props = (self.avisynth_version >= 8) and (global_vars.options['can_read_avisynth_props'] == True)
        self.readFrameProps = self.can_read_avisynth_props and readFrameProps

        if hasattr(env, 'get_error'):
            self.error_message = env.get_error()
            if self.error_message:
                return

        self.env = env
        if isinstance(script, avisynth.AVS_Clip):
            self.clip = script
        else:
            # vpy hack, remove when VapourSynth is supported
            if os.name == 'nt' and filename.endswith('.vpy'):
                if self.env.function_exists('AutoloadPlugins'): # AviSynth+
                    try:
                        self.env.invoke('AutoloadPlugins')
                    except avisynth.AvisynthError as err:
                        self.Framecount = oldFramecount
                        if not self.CreateErrorClip(err):
                            return
                if self.env.function_exists('VSImport'):
                    script = ur'VSImport("{0}", stacked=true)'.format(filename)
                else:
                    script = ur'AviSource("{0}")'.format(filename)
            scriptdirname, scriptbasename = os.path.split(filename)
            curdir = os.getcwdu()
            workdir = os.path.isdir(workdir) and workdir or scriptdirname
            if os.path.isdir(workdir):
                self.env.set_working_dir(workdir)
            self.env.set_global_var("$ScriptFile$", scriptbasename)
            self.env.set_global_var("$ScriptName$", filename)
            self.env.set_global_var("$ScriptDir$", scriptdirname + os.path.sep)
            try:
                #self.clip = self.env.invoke('Eval', [script, filename])

                ### split clip
                arg1 = arg2 = filterarg = ''
                found = arg2found = end = False

                # it's fast ~2-4 ms for 500 lines if split found else < 1 ms
                if script.find('/**avsp_split') > -1: # faster if not present
                    for line in script.split('\n'):
                        if not found:
                            if line.lstrip().startswith('/**avsp_split'):
                                found = True
                                line = line.lstrip()
                                if line[len('/**avsp_split'):].strip().startswith('**/'):
                                    end = True
                                continue
                            arg1 += line + '\n'
                        else:
                            if not end:
                                if line.lstrip().startswith('**/'):
                                    end = True
                                    continue
                                if line.lstrip().startswith('#'):
                                    filterarg += '\n'
                                else:
                                    filterarg += line + '\n'
                            else:
                                if not arg2found:
                                    _line = line.strip()
                                    if _line and not _line.startswith('#'):
                                        arg2found = True
                                arg2 += line + '\n' # always put it in arg2 or avisynth error line doesnt match the script
                    filterarg = filterarg.strip()
                    if not end:
                        arg1 = arg2 =  ''
                    elif found and arg1 and not arg2found:
                        arg2 += '\nlast'

                if arg1 and arg2:
                    self.split_clip = self.env.invoke('Eval', [arg1, filename])
                    if not isinstance(self.split_clip, avisynth.AVS_Clip):
                        self.split_clip = None
                    if filterarg and self.split_clip:
                        self.clip = self.env.invoke('Eval', [self.split_clip, arg2])
                        if not isinstance(self.clip, avisynth.AVS_Clip):
                            self.clip = self.env.invoke('Eval', [self.split_clip, arg2+'\nlast'])
                        if isinstance(self.clip, avisynth.AVS_Clip):
                            self.split_clip = self.env.invoke('Eval', [self.split_clip, filterarg])
                            if not isinstance(self.split_clip, avisynth.AVS_Clip):
                                self.clip = None
                    elif self.split_clip:
                        self.clip = self.env.invoke('Eval', [self.split_clip, arg2])
                        if not isinstance(self.clip, avisynth.AVS_Clip):
                            self.clip = self.env.invoke('Eval', [self.split_clip, arg2+'\nlast'])

                    if not isinstance(self.clip, avisynth.AVS_Clip):
                        self.split_clip = None
                        self.clip = self.env.invoke('Eval', [script, filename])
                else:
                    self.clip = self.env.invoke('Eval', [script, filename])
                ### split clip end

                if not isinstance(self.clip, avisynth.AVS_Clip):
                    raise avisynth.AvisynthError("Not a clip")
            except avisynth.AvisynthError as err:
                self.Framecount = oldFramecount
                self.split_clip = None
                if not self.CreateErrorClip(err):
                    return
            finally:
                os.chdir(curdir)
            try:
                if not isinstance(self.env.get_var("last"), avisynth.AVS_Clip):
                    self.env.set_var("last", self.clip)
            except avisynth.AvisynthError as err:
                if str(err) != 'NotFound':
                    raise
                self.env.set_var("last", self.clip)
            self.env.set_var("avsp_raw_clip", self.clip)
            if self.env.function_exists('AutoloadPlugins'): # AviSynth+
                try:
                    self.env.invoke('AutoloadPlugins')
                except avisynth.AvisynthError as err:
                    self.Framecount = oldFramecount
                    if not self.CreateErrorClip(err):
                        return

        # Set the video properties
        self.vi = self.clip.get_video_info()
        self.HasVideo = self.vi.has_video()
        if not self.HasVideo:
            self.clip = None
            errText = 'MessageClip("No video")'
            try:
                self.clip = self.env.invoke('Eval', errText)
                if not isinstance(self.clip, avisynth.AVS_Clip):
                    raise avisynth.AvisynthError("Not a clip")
            except avisynth.AvisynthError as err:
                return
            try:
                if not isinstance(self.env.get_var('last'), avisynth.AVS_Clip):
                    self.env.set_var('last', self.clip)
            except avisynth.AvisynthError as err:
                if str(err) != 'NotFound':
                    raise
                self.env.set_var('last', self.clip)
            self.vi=self.clip.get_video_info()
            self.HasVideo = self.vi.has_video()
        self.Framecount = self.vi.num_frames
        self.Width = self.vi.width
        self.Height = self.vi.height

        if (self.vi.is_yuv() or self.vi.is_yuva()) and not self.vi.is_y():
            self.WidthSubsampling = self.vi.get_plane_width_subsampling(avisynth.avs.AVS_PLANAR_U)
            self.HeightSubsampling = self.vi.get_plane_height_subsampling(avisynth.avs.AVS_PLANAR_U)
        self.DisplayWidth, self.DisplayHeight = self.Width, self.Height
        self.FramerateNumerator = self.vi.fps_numerator
        self.FramerateDenominator = self.vi.fps_denominator
        try:
            self.Framerate = self.vi.fps_numerator / float(self.vi.fps_denominator)
        except ZeroDivisionError:
            pass
        self.sample_type_dict = {
            avisynth.avs.AVS_SAMPLE_INT8: 8,
            avisynth.avs.AVS_SAMPLE_INT16: 16,
            avisynth.avs.AVS_SAMPLE_INT24: 24,
            avisynth.avs.AVS_SAMPLE_INT32: 32,
            avisynth.avs.AVS_SAMPLE_FLOAT: 32,
        }
        self.Audiorate = self.vi.audio_samples_per_second
        self.Audiolength = self.vi.num_audio_samples
        self.Audiochannels = self.vi.nchannels
        self.Audiobits = self.sample_type_dict.get(self.vi.sample_type, 0)
        self.IsAudioFloat = self.vi.sample_type == avisynth.avs.AVS_SAMPLE_FLOAT
        self.IsAudioInt = not self.IsAudioFloat
        self.IsRGB = self.vi.is_rgb()
        self.IsRGB24 = self.vi.is_rgb24()
        self.IsRGB32 = self.vi.is_rgb32()
        self.IsRGB48 = self.vi.is_rgb48()
        self.IsRGB64 = self.vi.is_rgb64()
        self.IsPlanar = self.vi.is_planar()
        self.IsPlanarRGBA = self.vi.is_planar_rgba()
        self.IsYUV = self.vi.is_yuv()
        self.IsYUVA = self.vi.is_yuva()
        self.IsYUY2 = self.vi.is_yuy2()
        self.IsYV24 = self.vi.is_yv24()
        self.IsYV16 = self.vi.is_yv16()
        self.IsYV12 = self.vi.is_yv12()
        self.IsYV411 = self.vi.is_yv411()
        self.IsY = self.vi.is_y()
        self.IsY8 = self.vi.is_y8()
        self.bits_per_component = self.vi.bits_per_component() # 8,10,12,14,16,32
        self.component_size = self.vi.component_size() # 1, 2, 4 (in bytes)
        self.num_components = self.vi.num_components() # 1-4
        self.IsRGBA = self.IsRGB32 or self.IsRGB64 or self.IsPlanarRGBA


        # Possible even for classic avs:
        '''
        self.Is444 = self.vi.is_444() # use this one instead of IsYV24
        self.Is422 = self.vi.is_422() # use this one instead of IsYV16
        self.Is420 = self.vi.is_420() # use this one instead of IsYV12
        '''
        # GPo, avs plus get colorspace
        cName = ''
        if self.env.function_exists('PixelType') and self.clip:
            cName = self.env.invoke("PixelType", self.clip)
            #cName = avs_plus_get_colorspace_name(self.vi.pixel_type)
        if cName:
            self.Colorspace = (cName*True)
        else:
            self.Colorspace = ('RGB24'*self.IsRGB24 + 'RGB32'*self.IsRGB32 + 'YUY2'*self.IsYUY2 + 'YV12'*self.IsYV12 +
                               'YV24'*self.IsYV24 + 'YV16'*self.IsYV16 + 'YV411'*self.IsYV411 + 'Y8'*self.IsY8
                               )

        self.IsFieldBased = self.vi.is_field_based()
        self.IsFrameBased = not self.IsFieldBased
        self.GetParity = self.clip.get_parity(0)
        self.HasAudio = self.vi.has_audio()
        self.interlaced = interlaced

        if display_clip and not self.CreateDisplayClip(matrix, interlaced, swapuv, bit_depth, readmatrix, killFilterClip=True, killSplitClip=False):
            return
        # GPo, no clue for wath it is and is it compatible with Planar or 16bit
        # must check it later
        if self.IsRGB and reorder_rgb:
            self.clip = self.BGR2RGB(self.clip)

        self.initialized = True

        if __debug__:
            print(u"AviSynth clip created successfully: '{0}'".format(self.name))

    def __del__(self):
        self.preview_filter = None
        if self.initialized or self.env and isinstance(self.env, avisynth.AVS_ScriptEnvironment):
            self.display_frame = None
            self.src_frame = None
            self.env.set_var("avsp_raw_clip", None)
            self.env.set_var("avsp_filter_clip", None)
            self.display_clip = None
            self.clip = None
            self.split_clip = None
            self.env = None # GPo new, we creating always a new env (its slower but avoid problems)
            self.initialized = False
            self.properties = ''
            if __debug__:
                print(u"Deleting allocated video memory for '{0}'".format(self.name))

    def CreateErrorClip(self, err='', display_clip_error=False):
        if self.preview_filter:
            self.preview_filter = None
            if not self.callBack('preview', -1):
                self.env.set_var("avsp_filter_clip", None)
        fontFace, fontSize, fontColor = global_vars.options['errormessagefont'][:3]   # GPo fontColor
        if fontColor == '':
            fontColor = '$FF0000'

        if display_clip_error:
            if not err:
                err = _('Error trying to display the clip')
                if self.bit_depth:
                    err += '\n' + _('Is bit-depth set correctly?')
                if self.resizeFilter:
                    err += '\n' + _('Is resample filter insert correctly?')
                if self.displayFilter:
                    err += '\n' + _('Is display filter set correctly?')
            else:
                err = str(err)
                #self.error_message = err
        else:
            err = str(err)
            self.error_message = err
        lineList = []
        yLine = 0
        nChars = 0
        for errLine in err.split('\n'):
            lineList.append('Subtitle("""%s""",y=%i,font="%s",size=%i,text_color=%s,align=8)' %
                (errLine, yLine, fontFace.encode(sys.getfilesystemencoding()), fontSize, fontColor))   # GPo fontColor
            yLine += fontSize
            nChars = max(nChars, len(errLine))
        eLength = self.Framecount
        eWidth = nChars * fontSize / 2
        eHeight = yLine + fontSize / 4
        firstLine = 'BlankClip(length=%(eLength)i,width=%(eWidth)i,height=%(eHeight)i)' % locals()
        errText = firstLine + '.'.join(lineList)
        try:
            clip = self.env.invoke('Eval', errText)
            if not isinstance(clip, avisynth.AVS_Clip):
                raise avisynth.AvisynthError("Not a clip")
            if display_clip_error:
                self.display_clip = clip
                vi = self.display_clip.get_video_info()
                self.DisplayWidth = vi.width
                self.DisplayHeight = vi.height# + 8
            else:
                self.clip = clip
        except avisynth.AvisynthError as err:
            return False
        self.callBack('errorclip', 0)
        return True

    def CreateDisplayClip(self, matrix=['auto', 'tv'], interlaced=None, swapuv=False, bit_depth=None,
                            readmatrix=False, killFilterClip=True, killSplitClip=False):

        if self.preview_filter and killFilterClip:
            self.KillFilterClip(createDisplayClip=False)
            self.callBack('preview', -1)

        """ TODO
        if self.preview_filter:
            if killFilterClip:
                self.preview_filter = None
                self.callBack('preview', -1):
            else:
                re, err = self.CreateFilterClip(self.preview_filter)
                if re and not err:
                    return True
                else:
                    self.callBack('preview', -1):
        """
        if self.IsSplitClip:
            self.IsSplitClip = None
            if killSplitClip:
                self.callBack('splitclip', -1)
            elif self.split_clip:
                re = self.SetSplitClip(True, createDisplayClip=False)
                if re:
                    return True
                else:
                    self.callBack('splitclip', -1)

        self.current_frame = -1
        self.display_clip = None
        self.display_clip = self.clip
        self.RGB48 = False
        self.bit_depth = bit_depth

        if bit_depth and not self.preview_filter:
            try:
                if bit_depth == 'rgb48': # TODO
                    if self.IsYV12:
                        self.RGB48 = True
                        self.DisplayWidth /= 2
                        self.DisplayHeight /= 2
                        return True
                elif self.IsYV12 or self.IsYV24 or self.IsY8:
                    if bit_depth == 's16':
                        args = [self.display_clip, 0, 0, 0, self.Height / 2]
                        self.display_clip = self.env.invoke('Crop', args)
                    elif bit_depth == 's10':
                        if self.env.function_exists('mt_lutxy'):
                            args = (
                            'avsp_raw_clip\n'
                            'msb = Crop(0, 0, Width(), Height() / 2)\n'
                            'lsb = Crop(0, Height() / 2, Width(), Height() / 2)\n'
                            'mt_lutxy(msb, lsb, "x 8 << y + 2 >>", chroma="process")')
                            self.display_clip = self.env.invoke('Eval', args)
                    elif bit_depth == 'i16':
                        args = ('avsp_raw_clip.AssumeBFF().TurnLeft().SeparateFields().'
                                'TurnRight().AssumeFrameBased().SelectOdd()')
                        self.display_clip = self.env.invoke('Eval', args)
                    elif bit_depth == 'i10':
                        if self.env.function_exists('mt_lutxy'):
                            args = (
                            'avsp_raw_clip.AssumeBFF().TurnLeft().SeparateFields().TurnRight().AssumeFrameBased()\n'
                            'mt_lutxy(SelectOdd(), SelectEven(), "x 8 << y + 2 >>", chroma="process")')
                            self.display_clip = self.env.invoke('Eval', args)
                    if not isinstance(self.display_clip, avisynth.AVS_Clip):
                        raise avisynth.AvisynthError("Not a clip")
            except avisynth.AvisynthError as err:
                return self.CreateErrorClip(display_clip_error=True)

        if isinstance(matrix, basestring):
            self.matrix = matrix
        else:
            if readmatrix:
                self.matrix_found = self.GetMatrix()
                if self.matrix_found is not None:
                    matrix = self.matrix_found[:]
                else: matrix = matrix[:]
            else:
                matrix = matrix[:]
                #self.matrix_found = None # GPo new, None only on create new clip

            if matrix[0] == 'auto':
                if self.DisplayWidth > 1024 or self.DisplayHeight > 576:
                    matrix[0] = '709'
                else:
                    matrix[0] = '601'
            matrix[1] = 'Rec' if matrix[1] == 'tv' else 'PC.'
            self.matrix = matrix[1] + matrix[0]

        if interlaced is not None:
            self.interlaced = interlaced
        if swapuv and self.IsYUV and not self.IsY:
            try:
                self.display_clip = self.env.invoke('SwapUV', self.display_clip)
            except avisynth.AvisynthError as err:
                return self.CreateErrorClip(display_clip_error=True)

        # display and resize filter
        args = ''
        #if self.preview_filter and not killFilterClip: # GPo new test
            #args = self.preview_filter + '\n'

        if self.displayFilter:
            args += self.displayFilter + '\n'

        if self.resizeFilter:
            rf = self.CalcResizeFilter()
            if rf:
                args += '%s(%i,%i)' % (rf[0], rf[1], rf[2])
        if args:
            try:
                self.display_clip = self.env.invoke('Eval', [self.display_clip, args])
            except:
                try:
                    err = self.error_message or self.display_clip.get_error()
                except:
                    err = None
                if not err:
                    err = self.env.get_error()
                if not err:
                    err = "Unknown Display or Resize filter error: Cannot create display clip"
                else:
                    err = 'Display or Resize filter error:\n' + str(err)
                return self.CreateErrorClip(err=err, display_clip_error=True)
            if not isinstance(self.display_clip, avisynth.AVS_Clip):
                err = "Unknown Display or Resize filter error: Cannot create display clip"
                return self.CreateErrorClip(err=err, display_clip_error=True)

        vi = self.display_clip.get_video_info()
        self.DisplayWidth = vi.width
        self.DisplayHeight = vi.height

        if vi.num_frames != self.Framecount:
            err = "Display filter error: Display-Clip length different"
            return self.CreateErrorClip(err=err, display_clip_error=True)

        self.convert_to_rgb_error = None
        if not self._ConvertToRGB():
            err = self.convert_to_rgb_error
            if not err:
                err = 'Display clip error ConvertToRGB32\n' + str(self.env.get_error())
            return self.CreateErrorClip(err=err, display_clip_error=True)
        elif self.convert_to_rgb_error:
            self.callBack('displayerror', self.convert_to_rgb_error)
        return True

    def CreateFilterClip(self, f_args=''):
        err = ''
        self.preview_filter = None
        if not f_args or not self.clip or self.IsErrorClip():
            return None, ''
        if self.IsSplitClip:
            self.IsSplitClip = None
            self.callBack('splitclip', -1)

        #self.env.set_var("avsp_filter_clip", None)
        self.env.set_var("avsp_filter_clip", self.clip)

        args = ('avsp_filter_clip\n' + f_args)
        if self.displayFilter:
            args += '\n' + self.displayFilter

        if self.resizeFilter:
            rf = self.CalcResizeFilter()
            if rf:
                args += '\n%s(%i,%i)' % (rf[0], rf[1], rf[2])
        try:
            clip = self.env.invoke("Eval", args)
        except:
            if self.error_message is None:
                err = self.env.get_error()
                if not err:
                    err = "Preview filter error: Not a clip"
            self.env.set_var("avsp_filter_clip", None)
            return None, err

        if not isinstance(clip, avisynth.AVS_Clip):
            if self.error_message is None:
                err = "Unknown Preview filter error: Not a clip"
            self.env.set_var("avsp_filter_clip", None)
            return None, err

        args = [clip, self.matrix, self.interlaced]
        try:
            clip = self.env.invoke("ConvertToRGB32", args)
        except:
            err = "Preview filter error: ConvertToRGB failed"
            clip = None
            self.env.set_var("avsp_filter_clip", None)
            return None, err
        if not isinstance(clip, avisynth.AVS_Clip):
            err = "Preview filter error: ConvertToRGB failed"
            self.env.set_var("avsp_filter_clip", None)
            return None, err

        vi = clip.get_video_info()
        if vi.num_frames != self.Framecount:
            clip = None
            err = "Preview filter error: \nPreview-Clip length different"
            self.env.set_var("avsp_filter_clip", None)
            return None, err

        framenr = self.current_frame
        if framenr < 0:
            framenr = 0
        frame = clip.get_frame(framenr)
        err = clip.get_error()
        if err:
            clip = None
            frame = None
            self.env.set_var("avsp_filter_clip", None)
            return None, err

        self.preview_filter = f_args
        self.display_clip = clip
        self.display_frame = frame
        self.display_pitch = self.display_frame.get_pitch()
        self.pBits = self.display_frame.get_read_ptr()
        return True, ''

    def KillFilterClip(self, createDisplayClip=True):
        self.preview_filter = None
        if not self.initialized:
            return
        try:
            if isinstance(self.env.get_var("avsp_filter_clip"), avisynth.AVS_Clip):
                self.env.set_var("avsp_filter_clip", None)
                if createDisplayClip:
                    self.CreateDisplayClip(self.matrix, self.interlaced, self.swapuv, self.bit_depth)
        except:
            pass

    # for avisynth from H8 but lower then 3.71 (bug C Interface)
    def GetMatrix_2(self):
        def _get_matrix():
            re = -1
            try:
                self.env.set_global_var("avsp_var", -1)
                self.env.set_var("avsp_var_clip", self.clip)
                args = ('avsp_var_clip\nScriptClip("""Global avsp_var=propGetInt("_Matrix")""")')
                clip = self.env.invoke("Eval", args)
                if isinstance(clip, avisynth.AVS_Clip) and clip.get_error() is None:
                    if self.current_frame > -1:
                        nr = min(self.current_frame, self.Framecount-1)
                    else: nr = 0
                    frame = clip.get_frame(nr)
                    try:
                        re = self.env.get_var("avsp_var", None)
                        self.env.set_var("avsp_var_clip", None)
                    except:
                        re = -1
            except:
                pass
            clip = frame = None
            return re

        matrix = None
        if self.clip and not self.IsErrorClip() and self.env.function_exists('propGetInt'): #self.avisynth_version >= 8:
            m = _get_matrix()
            if m in (1, 5, 6, 7):
                matrix = ['709','tv'] if m in (1,7) else ['601','tv']
            self.sourceMatrix = func.GetMatrixName(m)
        return matrix

    def GetMatrix(self):
        def _get_matrix():
            re = -1
            try:
                if self.current_frame > -1:
                    nr = min(self.current_frame, self.Framecount-1)
                else: nr = 0
                frame = self.clip.get_frame(nr)
                if self.clip.get_error() is None:
                    re = self.env.props_get_matrix(frame)
            except:
                pass
            frame = None
            return re

        matrix = None
        if self.clip and not self.IsErrorClip() and self.avisynth_version >= 8:
            if self.can_read_avisynth_props:
                m = _get_matrix()
            else:
                return self.GetMatrix_2()
            if m in (1, 5, 6, 7):
                matrix = ['709','tv'] if m in (1,7) else ['601','tv']
            self.sourceMatrix = func.GetMatrixName(m)
        return matrix

    # Only switch readFrameProps on/off here, do not set AVI.readFrameProps = True
    def SetReadFrameProps(self, enabled, callBack=True, readNow=True):
        if not self.initialized or not self.can_read_avisynth_props:
            self.readFrameProps = False
            self.properties = ''
            return
        if self.clip and not self.IsErrorClip():
            if enabled and readNow:
                self.properties = 'Frame: ' + str(self.current_frame) + '\n' + self.env.props_get_all(self.src_frame)
        else:
            self.properties = ''
        self.readFrameProps = enabled
        if not enabled:
            self.properties = ''
        if callBack:
            self.callBack(ident='property', value=self.properties, framenr=-1)

    # resize filter must be a tuple (filter string, resize W, resize H, zoom, fit height, isScrollbar visible)
    # set rfilter to None to remove the resize filter
    def SetResizeFilter(self, rfilter):
        if rfilter:
            try:
                f,dw,dh,zoom,fit,hidescroll = rfilter
            except:
                return
        self.resizeFilter = rfilter
        return True

    def SetSplitClip(self, enabled, createDisplayClip=True):
        if (self.IsSplitClip and enabled) or (not self.IsSplitClip and not enabled):
            return True
        self.IsSplitClip = None
        if self.split_clip:
            if enabled:
                framenr = self.current_frame
                if framenr < 0:
                    framenr = 0
                #vi = self.split_clip.get_video_info()
                #framenr = min(self.Framecount-1, vi.num_frames-1)
                frame = self.split_clip.get_frame(framenr)
                err = self.split_clip.get_error()
                if err:
                    #self.split_clip = None # must test!!! if self.clip then corrupt? if not, we can remove IsSplitClip
                    frame = None
                    return

                # create the split display clip
                args = [self.split_clip, self.matrix, self.interlaced]
                try:
                    self.display_clip = self.env.invoke("ConvertToRGB32", args)
                    if not isinstance(self.display_clip, avisynth.AVS_Clip):
                        raise
                except:
                    #self.split_clip = None # must test!!! if self.clip then corrupt? if not, we can remove IsSplitClip
                    if createDisplayClip:
                        self.CreateDisplayClip(self.matrix, self.interlaced, self.swapuv, self.bit_depth, killSplitClip=True)
                    return

                if self.resizeFilter:
                    rf = self.CalcResizeFilter()
                    if rf:
                        args = '%s(%i,%i)' % (rf[0], rf[1], rf[2])
                        self.display_clip = self.env.invoke('Eval', [self.display_clip, args])

                # disable all preview filters
                if self.preview_filter:
                    self.KillFilterClip(createDisplayClip=False)
                    self.callBack('preview', -1) # reset avsp menus (disable preview filter)

                self.current_frame = -1 # get the frame new
                self.display_frame = frame
                self.display_pitch = self.display_frame.get_pitch()
                self.pBits = self.display_frame.get_read_ptr()
                self.IsSplitClip = True
                return True
            else:
                if not self.IsErrorClip() and createDisplayClip:
                    return self.CreateDisplayClip(self.matrix, self.interlaced, self.swapuv, self.bit_depth, killSplitClip=True)

    def _GetFrame(self, frame):
        def Error():
            if self.readFrameProps and self.avisynth_version >= 8:
                self.properties = 'Get frame %i error' % frame

        if self.initialized:
            if self.current_frame == frame:
                return True
            if frame < 0:
                frame = 0
            if frame >= self.Framecount:
                frame = self.Framecount - 1
                if self.current_frame == frame:
                    return True
            # Original clip
            if not self.IsSplitClip or not self.split_clip:
                self.src_frame = self.clip.get_frame(frame)
                if self.clip.get_error():
                    Error()
                    return False
            else:  # split_clip
                self.src_frame = self.split_clip.get_frame(frame)
                if self.split_clip.get_error():
                    Error()
                    return False

            self.pitch = self.src_frame.get_pitch()
            self.pitchUV = self.src_frame.get_pitch(avisynth.avs.AVS_PLANAR_U)
            self.ptrY = self.src_frame.get_read_ptr()
            if not self.IsY:
                self.ptrU = self.src_frame.get_read_ptr(avisynth.avs.AVS_PLANAR_U)
                self.ptrV = self.src_frame.get_read_ptr(avisynth.avs.AVS_PLANAR_V)
                if self.num_components == 4 and self.IsPlanar:
                    self.ptrA = self.src_frame.get_read_ptr(avisynth.avs.AVS_PLANAR_A)

            # Display clip
            if self.display_clip:
                self.display_frame = self.display_clip.get_frame(frame)
                if self.display_clip.get_error():
                    Error()
                    return False
                self.display_pitch = self.display_frame.get_pitch()
                self.pBits = self.display_frame.get_read_ptr()

            ## getProps
            if self.readFrameProps:
                self.properties = 'Frame: ' + str(frame) + '\n' + self.env.props_get_all(self.src_frame)

            self.current_frame = frame
            return True
        return False

    # coded: pfmod 2021
    def GetPixelYUV(self, x, y):
        # if a resize filter used in the preview filter. CRASH if not check here
        if self.DisplayWidth != self.Width or self.DisplayHeight != self.Height:
            return (-1,-1,-1)
        if self.IsPlanar:
            indexY = x * self.component_size + y * self.pitch
            # IsY8 does not detect Y10..Y16,Y32
            # Probably IsY is not implemented, so we use num_components
            if self.num_components == 1: # GPo, It is, but num_components is just as good
                if self.bits_per_component == 8:
                    return (self.ptrY[indexY], -1, -1)
                elif self.bits_per_component <= 16:
                    bufferY = [self.ptrY[indexY], self.ptrY[indexY + 1]]
                    valY = struct.unpack('=H', bytearray(bufferY))[0]
                    return (valY, -1, -1)
                else:
                    bufferY = [self.ptrY[indexY], self.ptrY[indexY + 1], self.ptrY[indexY + 2], self.ptrY[indexY + 3]]
                    valY = struct.unpack('=f', bytearray(bufferY))[0]
                    return (valY, -1, -1)
            x = x >> self.WidthSubsampling
            y = y >> self.HeightSubsampling
            indexU = indexV = x * self.component_size + y * self.pitchUV
        elif self.IsYUY2:
            indexY = (x*2) + y * self.pitch
            indexU = 4*(x/2) + 1 + y * self.pitch
            indexV = 4*(x/2) + 3 + y * self.pitch
        else:
            return (-1,-1,-1)
        if self.bits_per_component == 8:
            return (self.ptrY[indexY], self.ptrU[indexU], self.ptrV[indexV])
        if self.bits_per_component <= 16:
            # struct.unpack needs import struct, and returns a single element tuple
            # =H: unsigned short (2 bytes), native byte order
            bufferY = [self.ptrY[indexY], self.ptrY[indexY + 1]]
            valY = struct.unpack('=H', bytearray(bufferY))[0]
            bufferU = [self.ptrU[indexU], self.ptrU[indexU + 1]]
            valU = struct.unpack('=H', bytearray(bufferU))[0]
            bufferV = [self.ptrV[indexV], self.ptrV[indexV + 1]]
            valV = struct.unpack('=H', bytearray(bufferV))[0]
            return (valY, valU, valV)
        #float # =f: float (4 bytes), native byte order
        bufferY = [self.ptrY[indexY], self.ptrY[indexY + 1], self.ptrY[indexY + 2], self.ptrY[indexY + 3]]
        valY = struct.unpack('=f', bytearray(bufferY))[0]
        bufferU = [self.ptrU[indexU], self.ptrU[indexU + 1], self.ptrU[indexU + 2], self.ptrU[indexU + 3]]
        valU = struct.unpack('=f', bytearray(bufferU))[0]
        bufferV = [self.ptrV[indexV], self.ptrV[indexV + 1], self.ptrV[indexV + 2], self.ptrV[indexV + 3]]
        valV = struct.unpack('=f', bytearray(bufferV))[0]
        return (valY, valU, valV)

    def GetPixelYUVA(self, x, y):
        # if a resize filter used in the preview filter. CRASH if not check here
        if self.DisplayWidth != self.Width or self.DisplayHeight != self.Height:
            return (-1,-1,-1,-1)
        indexY = indexA = x * self.component_size + y * self.pitch
        x = x >> self.WidthSubsampling
        y = y >> self.HeightSubsampling
        indexU = indexV = x * self.component_size + y * self.pitchUV
        if self.bits_per_component == 8:
            return (self.ptrY[indexY], self.ptrU[indexU], self.ptrV[indexV], self.ptrA[indexA])
        if self.bits_per_component <= 16:
            bufferY = [self.ptrY[indexY], self.ptrY[indexY + 1]]
            valY = struct.unpack('=H', bytearray(bufferY))[0]
            bufferU = [self.ptrU[indexU], self.ptrU[indexU + 1]]
            valU = struct.unpack('=H', bytearray(bufferU))[0]
            bufferV = [self.ptrV[indexV], self.ptrV[indexV + 1]]
            valV = struct.unpack('=H', bytearray(bufferV))[0]
            bufferA = [self.ptrA[indexA], self.ptrA[indexA + 1]]
            valA = struct.unpack('=H', bytearray(bufferA))[0]
            return (valY, valU, valV, valA)
        # 32bit
        bufferY = [self.ptrY[indexY], self.ptrY[indexY + 1], self.ptrY[indexY + 2], self.ptrY[indexY + 3]]
        valY = struct.unpack('=f', bytearray(bufferY))[0]
        bufferU = [self.ptrU[indexU], self.ptrU[indexU + 1], self.ptrU[indexU + 2], self.ptrU[indexU + 3]]
        valU = struct.unpack('=f', bytearray(bufferU))[0]
        bufferV = [self.ptrV[indexV], self.ptrV[indexV + 1], self.ptrV[indexV + 2], self.ptrV[indexV + 3]]
        valV = struct.unpack('=f', bytearray(bufferV))[0]
        bufferA = [self.ptrA[indexA], self.ptrA[indexA + 1], self.ptrA[indexA + 2], self.ptrA[indexA + 3]]
        valA = struct.unpack('=f', bytearray(bufferA))[0]
        return (valY, valU, valV, valA)

    def GetPixelRGB(self, x, y, BGR=True):
        if self.IsRGB:
            # if a resize filter used in the preview filter. CRASH if not check here
            if self.DisplayWidth != self.Width or self.DisplayHeight != self.Height:
                return (-1,-1,-1)
            if self.IsPlanar: # plane order is GBR
                index = x * self.component_size + y * self.pitch
                if self.component_size == 1: # 8bit
                    return (self.ptrV[index], self.ptrY[index], self.ptrU[index])
                elif self.component_size == 2: # 10 to 16bit
                    bufferG = [self.ptrY[index], self.ptrY[index + 1]]
                    valG = struct.unpack('=H', bytearray(bufferG))[0]
                    bufferB = [self.ptrU[index], self.ptrU[index + 1]]
                    valB = struct.unpack('=H', bytearray(bufferB))[0]
                    bufferR = [self.ptrV[index], self.ptrV[index + 1]]
                    valR = struct.unpack('=H', bytearray(bufferR))[0]
                else: # 32bit
                    bufferG = [self.ptrY[index], self.ptrY[index + 1], self.ptrY[index + 2], self.ptrY[index + 3]]
                    valG = struct.unpack('=f', bytearray(bufferG))[0]
                    bufferB = [self.ptrU[index], self.ptrU[index + 1], self.ptrU[index + 2], self.ptrU[index + 3]]
                    valB = struct.unpack('=f', bytearray(bufferB))[0]
                    bufferR = [self.ptrV[index], self.ptrV[index + 1], self.ptrV[index + 2], self.ptrV[index + 3]]
                    valR = struct.unpack('=f', bytearray(bufferR))[0]
                return (valR, valG, valB)

            bytes = self.vi.bytes_from_pixels(1)
            if self.bits_per_component == 16: # return also RGB48 and RGB64 if needed
                #x = x * 8 64bit
                #x = x * 6 48bit
                if BGR:
                    indexB = (x * bytes) + (self.Height - 1 - y) * self.pitch # same for 48, 64 bit
                    bufferB = [self.ptrY[indexB], self.ptrY[indexB+1]]
                    valB = struct.unpack('=H', bytearray(bufferB))[0]
                    bufferG = [self.ptrY[indexB+2], self.ptrY[indexB+3]]
                    valG = struct.unpack('=H', bytearray(bufferG))[0]
                    bufferR = [self.ptrY[indexB+4], self.ptrY[indexB+5]]
                    valR = struct.unpack('=H', bytearray(bufferR))[0]
                    return (valR, valG, valB)
                else:
                    indexR = (x * bytes) + y * self.pitch
                    bufferR = [self.ptrY[indexR], self.ptrY[indexR+1]]
                    valR = struct.unpack('=H', bytearray(bufferR))[0]
                    bufferG = [self.ptrY[indexR+2], self.ptrY[indexR+3]]
                    valG = struct.unpack('=H', bytearray(bufferG))[0]
                    bufferB = [self.ptrY[indexR+4], self.ptrY[indexR+5]]
                    valB = struct.unpack('=H', bytearray(bufferB))[0]
                    return (valR, valG, valB)

            if self.bits_per_component == 8: # return also RGB24 and RGB32
                if BGR:
                    indexB = (x * bytes) + (self.Height - 1 - y) * self.pitch
                    indexG = indexB + 1
                    indexR = indexB + 2
                else:
                    indexR = (x * bytes) + y * self.pitch
                    indexG = indexR + 1
                    indexB = indexR + 2
                return (self.ptrY[indexR], self.ptrY[indexG], self.ptrY[indexB])

        return (-1,-1,-1)

    def GetPixelRGBA(self, x, y, BGR=True):
        # if a resize filter used in the preview filter. CRASH if not check here
        if self.DisplayWidth != self.Width or self.DisplayHeight != self.Height:
            return (-1,-1,-1,-1)
        if not self.IsPlanarRGBA:
            if self.IsRGB32:
                bytes = self.vi.bytes_from_pixels(1)
                if BGR:
                    indexB = (x * bytes) + (self.Height - 1 - y) * self.pitch
                    indexG = indexB + 1
                    indexR = indexB + 2
                    indexA = indexB + 3
                else:
                    indexR = (x * bytes) + y * self.pitch
                    indexG = indexR + 1
                    indexB = indexR + 2
                    indexA = indexB + 3
                return (self.ptrY[indexR], self.ptrY[indexG], self.ptrY[indexB], self.ptrY[indexA])
            elif self.IsRGB64:
                bytes = self.vi.bytes_from_pixels(1)
                if BGR:
                    indexB = (x * bytes) + (self.Height - 1 - y) * self.pitch # same for 48, 64 bit
                    bufferB = [self.ptrY[indexB], self.ptrY[indexB+1]]
                    valB = struct.unpack('=H', bytearray(bufferB))[0]
                    bufferG = [self.ptrY[indexB+2], self.ptrY[indexB+3]]
                    valG = struct.unpack('=H', bytearray(bufferG))[0]
                    bufferR = [self.ptrY[indexB+4], self.ptrY[indexB+5]]
                    valR = struct.unpack('=H', bytearray(bufferR))[0]
                    bufferA = [self.ptrY[indexB+6], self.ptrY[indexB+7]]
                    valA = struct.unpack('=H', bytearray(bufferA))[0]
                else:
                    indexR = (x * bytes) + y * self.pitch
                    bufferR = [self.ptrY[indexR], self.ptrY[indexR+1]]
                    valR = struct.unpack('=H', bytearray(bufferR))[0]
                    bufferG = [self.ptrY[indexR+2], self.ptrY[indexR+3]]
                    valG = struct.unpack('=H', bytearray(bufferG))[0]
                    bufferB = [self.ptrY[indexR+4], self.ptrY[indexR+5]]
                    valB = struct.unpack('=H', bytearray(bufferB))[0]
                    bufferA = [self.ptrY[indexR+6], self.ptrY[indexR+7]]
                    valA = struct.unpack('=H', bytearray(bufferA))[0]
                return (valR, valG, valB, valA)
            else:
                return (-1, -1, -1, -1)
        else:
            # plane order is GBR
            index = x * self.component_size + y * self.pitch
            if self.component_size == 1: # 8bit
                return (self.ptrV[index], self.ptrY[index], self.ptrU[index], self.ptrA[index])
            elif self.component_size == 2: # 10 to 16bit
                bufferG = [self.ptrY[index], self.ptrY[index + 1]]
                valG = struct.unpack('=H', bytearray(bufferG))[0]
                bufferB = [self.ptrU[index], self.ptrU[index + 1]]
                valB = struct.unpack('=H', bytearray(bufferB))[0]
                bufferR = [self.ptrV[index], self.ptrV[index + 1]]
                valR = struct.unpack('=H', bytearray(bufferR))[0]
                bufferA = [self.ptrA[index], self.ptrA[index + 1]]
                valA = struct.unpack('=H', bytearray(bufferA))[0]
            else: # 32bit
                bufferG = [self.ptrY[index], self.ptrY[index + 1], self.ptrY[index + 2], self.ptrY[index + 3]]
                valG = struct.unpack('=f', bytearray(bufferG))[0]
                bufferB = [self.ptrU[index], self.ptrU[index + 1], self.ptrU[index + 2], self.ptrU[index + 3]]
                valB = struct.unpack('=f', bytearray(bufferB))[0]
                bufferR = [self.ptrV[index], self.ptrV[index + 1], self.ptrV[index + 2], self.ptrV[index + 3]]
                valR = struct.unpack('=f', bytearray(bufferR))[0]
                bufferA = [self.ptrA[index], self.ptrA[index + 1], self.ptrA[index + 2], self.ptrA[index + 3]]
                valA = struct.unpack('=f', bytearray(bufferA))[0]
            return (valR, valG, valB, valA)

    def GetVarType(self, str_var):
        try:
            return self.env.get_var(str_var, type=True)[1]
        except avisynth.AvisynthError:
            return None

    def IsErrorClip(self):
        return self.error_message is not None

    def BGR2RGB(self, clip):
        '''Reorder AviSynth's RGB (BGR) to RGB

        BGR -> RGB
        BGRA -> RGBA
        '''
        if self.IsRGB:
            clip = self.env.invoke("FlipVertical", clip)
            r = self.env.invoke("ShowRed", clip)
            b = self.env.invoke("ShowBlue", clip)
            if self.IsRGB24:
                return self.env.invoke("MergeRGB", [b, clip, r, 'RGB24'])
            else:
                return self.env.invoke("MergeARGB", [clip, b, clip, r])

    def Y4MHeader(self, colorspace=None, depth=None, width=None, height=None, sar='0:0', X=None):
        '''Return a header for a yuv4mpeg2 stream'''
        re_res = re.compile(r'([x*/])(\d+)')
        if width is None:
            width = self.Width
        elif isinstance(width, basestring):
            match = re_res.match(width)
            if match:
                if match.group(1) == '/':
                    width = self.Width / int(match.group(2))
                else:
                    width = self.Width * int(match.group(2))
            else:
                raise Exception(_('Invalid string: ') + width)
        if height is None:
            height = self.Height
        elif isinstance(height, basestring):
            match = re_res.match(height)
            if match:
                if match.group(1) == '/':
                    height = self.Height / int(match.group(2))
                else:
                    height = self.Height * int(match.group(2))
            else:
                raise Exception(_('Invalid string: ') + height)
        if self.interlaced:
            interlaced = 'b' if self.vi.is_bff() else 't'
        else:
            interlaced = 'p'
        colorspace_dict = {'YV24': '444',
                           'YV16': '422',
                           'YV12': '420',
                           'YV411': '411',
                           'Y8': 'mono'}
        if colorspace is None:
            if self.Colorspace not in colorspace_dict:
                raise Exception(_("{colorspace} can't be used with a yuv4mpeg2 "
                    "header.\nSpecify the right colorspace if piping fake video data.\n"
                    .format(colorspace=self.Colorspace)))
            colorspace = colorspace_dict[self.Colorspace]
        if depth:
            colorspace = 'p'.join((colorspace, str(depth)))
        X = ' X' + X if X is not None else ''
        return 'YUV4MPEG2 W{0} H{1} I{2} F{3}:{4} A{5} C{6}{7}\n'.format(width,
            height, interlaced, self.FramerateNumerator, self.FramerateDenominator,
            sar, colorspace, X)

    def RawFrame(self, frame, y4m_header=False):
        '''Get a buffer of raw video data'''
        if self.initialized:
            if frame < 0:
                frame = 0
            if frame >= self.Framecount:
                frame = self.Framecount - 1
            frame = self.clip.get_frame(frame)
            if self.clip.get_error():
                return
            total_bytes = self.Width * self.Height * self.vi.bits_per_pixel() >> 3
            if y4m_header is not False:
                X = ' X' + y4m_header if isinstance(y4m_header, basestring) else ''
                y4m_header = 'FRAME{0}\n'.format(X)
            else:
                y4m_header = ''
            y4m_header_len = len(y4m_header)
            buf = ctypes.create_string_buffer(total_bytes + y4m_header_len)
            buf[0:y4m_header_len] = y4m_header
            write_addr = ctypes.addressof(buf) + y4m_header_len
            P_UBYTE = ctypes.POINTER(ctypes.c_ubyte)
            if self.IsPlanar and not self.IsY:
                for plane in (avisynth.avs.AVS_PLANAR_Y, avisynth.avs.AVS_PLANAR_U, avisynth.avs.AVS_PLANAR_V):
                    if x86_64:
                        write_ptr = avisynth.ffi.cast('unsigned char *', write_addr)
                    else:
                        write_ptr = ctypes.cast(write_addr, P_UBYTE)
                    # using get_row_size(plane) and get_height(plane) breaks v2.5.8
                    width = frame.get_row_size() >> self.vi.get_plane_width_subsampling(plane)
                    height = frame.get_height() >> self.vi.get_plane_height_subsampling(plane)
                    self.env.bit_blt(write_ptr, width, frame.get_read_ptr(plane),
                                     frame.get_pitch(plane), width, height)
                    write_addr += width * height
            else:
                # Note that AviSynth uses BGR
                if x86_64:
                    write_ptr = avisynth.ffi.cast('unsigned char *', write_addr)
                else:
                    write_ptr = ctypes.cast(write_addr, P_UBYTE)
                self.env.bit_blt(write_ptr, frame.get_row_size(), frame.get_read_ptr(),
                            frame.get_pitch(), frame.get_row_size(), frame.get_height())
            return buf

    def AutocropFrame(self, frame, tol=70):
        '''Return crop values for a specific frame'''
        width, height = self.Width, self.Height
        if not self._GetFrame(frame):
            return
        GetPixelColor = self.GetPixelRGB if self.IsRGB else self.GetPixelYUV
        w, h = width - 1, height - 1
        top_left0, top_left1, top_left2 = GetPixelColor(0, 0)
        bottom_right0, bottom_right1, bottom_right2 = GetPixelColor(w, h)
        top = bottom = left = right = 0

        # top & bottom
        top_done = bottom_done = False
        for i in range(height):
            for j in range(width):
                if not top_done:
                    color0, color1, color2 = GetPixelColor(j, i)
                    if (abs(color0 - top_left0) > tol or
                        abs(color1 - top_left1) > tol or
                        abs(color2 - top_left2) > tol):
                            top = i
                            top_done = True
                if not bottom_done:
                    color0, color1, color2 = GetPixelColor(j, h - i)
                    if (abs(color0 - bottom_right0) > tol or
                        abs(color1 - bottom_right1) > tol or
                        abs(color2 - bottom_right2) > tol):
                            bottom = i
                            bottom_done = True
                if top_done and bottom_done: break
            else: continue
            break

        # left & right
        left_done = right_done = False
        for j in range(width):
            for i in range(height):
                if not left_done:
                    color0, color1, color2 = GetPixelColor(j, i)
                    if (abs(color0 - top_left0) > tol or
                        abs(color1 - top_left1) > tol or
                        abs(color2 - top_left2) > tol):
                            left = j
                            left_done = True
                if not right_done:
                    color0, color1, color2 = GetPixelColor(w - j, i)
                    if (abs(color0 - bottom_right0) > tol or
                        abs(color1 - bottom_right1) > tol or
                        abs(color2 - bottom_right2) > tol):
                            right = j
                            right_done = True
                if left_done and right_done: break
            else: continue
            break
        return left, top, right, bottom

    # calculate the resize values needed for the display clip for the given client area (dw, dh)
    def CalcResizeFilter(self):
        mod = 2 if not self.vi.is_yv411() else 4
        try:
            f, dw, dh, zoom, fitHeight, hidescrollbars = self.resizeFilter
        except:
            return
        if dw < 12 or dh < 12:
            return
        vW, vH = self.Width, self.Height
        ratio = float(vW)/vH
        if zoom == 1:
            factorWidth = float(dw) / vW
            factorHeight = float(dh) / vH
            if fitHeight or factorWidth >= factorHeight:
                H = int(float(dh)/mod)*mod
                W = int(float(H)*ratio/mod)*mod
                if fitHeight and not hidescrollbars and W > dw:
                    H -= utils.GetScrollbarMetric_X() - 2
                    H = int(float(H)/mod)*mod
                    W = int(float(H)*ratio/mod)*mod
            else:
                W = int(float(dw)/mod)*mod
                H = int(float(W)/ratio/mod)*mod
        else:
            W = round(vW* zoom) //mod*mod
            H = round(vH* zoom) //mod*mod
        # return if new size < 12 or zoomfactor > 2.5
        if W < 12 or H < 12 or (float(W + H) / (self.Width + self.Height) > 2.5):
            return
        return (f, W, H)

# on Windows is faster to use DrawDib (VFW)
if os.name == 'nt':

    # Define C types and constants
    DWORD = ctypes.c_ulong
    UINT = ctypes.c_uint
    WORD = ctypes.c_ushort
    LONG = ctypes.c_long
    BYTE = ctypes.c_byte
    CHAR = ctypes.c_char
    HANDLE = ctypes.c_ulong
    NULL = 0
    OF_READ = UINT(0)
    BI_RGB = 0
    GENERIC_WRITE = 0x40000000L
    CREATE_ALWAYS = 2
    FILE_ATTRIBUTE_NORMAL  = 0x00000080

    # Define C structures
    class RECT(ctypes.Structure):
        _fields_ = [("left", LONG),
                    ("top", LONG),
                    ("right", LONG),
                    ("bottom", LONG)]

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [("biSize",  DWORD),
                    ("biWidth",   LONG),
                    ("biHeight",   LONG),
                    ("biPlanes",   WORD),
                    ("biBitCount",   WORD),
                    ("biCompression",  DWORD),
                    ("biSizeImage",  DWORD),
                    ("biXPelsPerMeter",   LONG),
                    ("biYPelsPerMeter",   LONG),
                    ("biClrUsed",  DWORD),
                    ("biClrImportant",  DWORD)]

    class BITMAPFILEHEADER(ctypes.Structure):
        _fields_ = [
            ("bfType",    WORD),
            ("bfSize",   DWORD),
            ("bfReserved1",    WORD),
            ("bfReserved2",    WORD),
            ("bfOffBits",   DWORD)]

    def CreateBitmapInfoHeader(clip, bmih=None):
        vi = clip.get_video_info()
        if bmih is None:
            bmih = BITMAPINFOHEADER()
        bmih.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmih.biWidth = vi.width
        bmih.biHeight = vi.height
        bmih.biPlanes = 1
        if vi.is_rgb32():
            bmih.biBitCount = 32
        elif vi.is_rgb24():
            bmih.biBitCount = 24
        else: raise avisynth.AvisynthError("Input colorspace is not RGB24 or RGB32")
        bmih.biCompression = BI_RGB
        bmih.biSizeImage = 0 # ignored with biCompression == BI_RGB
        bmih.biXPelsPerMeter = 0
        bmih.biYPelsPerMeter = 0
        bmih.biClrUsed = 0
        bmih.biClrImportant = 0
        return bmih


    # Define C functions

    CreateFile = ctypes.windll.kernel32.CreateFileA
    WriteFile = ctypes.windll.kernel32.WriteFile
    CloseHandle = ctypes.windll.kernel32.CloseHandle

    DrawDibOpen = ctypes.windll.msvfw32.DrawDibOpen
    DrawDibClose = ctypes.windll.msvfw32.DrawDibClose
    DrawDibDraw = ctypes.windll.msvfw32.DrawDibDraw
    handleDib = [None]

    def InitRoutines():
        handleDib[0] = DrawDibOpen()

    def ExitRoutines():
        DrawDibClose(handleDib[0])


    class AvsClip(AvsClipBase):

        def CreateDisplayClip(self, *args, **kwargs):
            if not AvsClipBase.CreateDisplayClip(self, *args, **kwargs):
                return
            # Prepare info header for displaying
            self.bmih = BITMAPINFOHEADER()
            CreateBitmapInfoHeader(self.display_clip, self.bmih)
            self.pInfo = ctypes.pointer(self.bmih)
            return True

        # GPo, can removed, but then the filter clip must have the same dimensions as the display clip before
        def CreateFilterClip(self, *args, **kwargs):
            ret, err = AvsClipBase.CreateFilterClip(self, *args, **kwargs)
            if not ret:
                return ret, err
            # if dimensions changed, we need new bitmap header (it's a bit faster do not create it always)
            vi = self.display_clip.get_video_info()
            if vi.width != self.DisplayWidth or vi.height != self.DisplayHeight:
                self.DisplayWidth, self.DisplayHeight = vi.width, vi.height
                self.bmih = BITMAPINFOHEADER()
                CreateBitmapInfoHeader(self.display_clip, self.bmih)
                self.pInfo = ctypes.pointer(self.bmih)
            return True, ''

        def SetSplitClip(self, *args, **kwargs):
            re = AvsClipBase.SetSplitClip(self, *args, **kwargs)
            vi = self.display_clip.get_video_info()
            if vi.width != self.DisplayWidth or vi.height != self.DisplayHeight:
                self.DisplayWidth, self.DisplayHeight = vi.width, vi.height
                self.bmih = BITMAPINFOHEADER()
                CreateBitmapInfoHeader(self.display_clip, self.bmih)
                self.pInfo = ctypes.pointer(self.bmih)
            return re

        def GetMatrix(self):
            return AvsClipBase.GetMatrix(self)

        def _ConvertToRGB(self):
            if not self.IsRGB32: # bug in avisynth v2.6 alphas with ConvertToRGB24
                args = [self.display_clip, self.matrix, self.interlaced]
                try:
                    self.display_clip = self.env.invoke("ConvertToRGB32", args)
                except:
                    err = str(self.env.get_error())
                    if err:
                        self.convert_to_rgb_error = err + '\nTrying alternative RGB32 conversion'
                    else:
                        self.convert_to_rgb_error = 'Unknown convert to RGB32 error\n Trying alternative RGB32 conversion'

                    b_interlaced = 'True' if self.interlaced else 'False'
                    args = 'ConvertToYUV444(matrix="%s", interlaced=%s, ChromaInPlacement="left")\n' % (self.matrix, b_interlaced) + \
                           'ConvertToRGB32(matrix="%s", interlaced=%s)' % (self.matrix, b_interlaced)
                    try:
                        self.display_clip = self.env.invoke('Eval', [self.display_clip, args])
                    except avisynth.AvisynthError as err:
                        if self.convert_to_rgb_error:
                            self.convert_to_rgb_error += '\nAttempt failed !'
                        return False
                    if not isinstance(self.display_clip, avisynth.AVS_Clip):
                        if self.convert_to_rgb_error:
                            self.convert_to_rgb_error += '\nAttempt failed !'
                        return False
            return True

        def _GetFrame(self, frame):
            if AvsClipBase._GetFrame(self, frame):
                self.bmih.biWidth = self.display_pitch * 8 / self.bmih.biBitCount
                return True
            return False

        def DrawFrame(self, frame, dc=None, offset=(0,0), size=None, srcXY=(0,0)):
            if not self._GetFrame(frame):
                return
            if dc:
                hdc = dc.GetHDC()
                if size is None:
                    w = self.DisplayWidth
                    h = self.DisplayHeight
                else:
                    w, h = size
                row_size = self.display_frame.get_row_size()
                if self.display_pitch == row_size: # the size of the vfb is not guaranteed to be pitch * height unless pitch == row_size
                    pBits = self.pBits
                else:
                    buf = ctypes.create_string_buffer(self.display_pitch * self.DisplayHeight)
                    #pBits = ctypes.addressof(buf) # GPo, not for x64, buffer address can be too large
                    #pBits = ctypes.cast(buf, ctypes.POINTER(ctypes.c_ubyte))  # GPo, too slow
                    pBits = ctypes.pointer(buf) # GPo new
                    ctypes.memmove(pBits, self.pBits, self.display_pitch * (self.DisplayHeight - 1) + row_size)

                DrawDibDraw(handleDib[0], hdc, offset[0], offset[1], w, h,
                            self.pInfo, pBits, srcXY[0], srcXY[1], w, h, 0)
                return True

        """
        # GPo, alternativ, I see visual no problems, it is faster
        def DrawFrame(self, frame, dc=None, offset=(0,0), size=None, srcXY=(0,0)):
            if not self._GetFrame(frame):
                return
            if dc:
                hdc = dc.GetHDC()
                if size is None:
                    w = self.DisplayWidth
                    h = self.DisplayHeight
                else:
                    w, h = size
                DrawDibDraw(handleDib[0], hdc, offset[0], offset[1], w, h,
                            self.pInfo, self.pBits, srcXY[0], srcXY[1], w, h, 0)
                return True
         """

# Use generical wxPython drawing support on other platforms
else:

    import wx

    def InitRoutines():
        pass

    def ExitRoutines():
        pass


    class AvsClip(AvsClipBase):

        def _ConvertToRGB(self):
            # There's issues with RGB32, we convert to RGB24
            # AviSynth uses BGR ordering but we need RGB
            try:
                clip = self.display_clip
                if not self.IsRGB24:
                    args = [clip, self.matrix, self.interlaced]
                    clip = self.env.invoke("ConvertToRGB24", args)
                r = self.env.invoke("ShowRed", clip)
                b = self.env.invoke("ShowBlue", clip)
                merge_args = [b, clip, r, "RGB24"]
                self.display_clip = self.env.invoke("MergeRGB", merge_args)
                return True
            except avisynth.AvisynthError as err:
                return False

        def DrawFrame(self, frame, dc=None, offset=(0,0), size=None):
            if not self._GetFrame(frame):
                return
            if dc:
                if size is None:
                    w = self.DisplayWidth
                    h = self.DisplayHeight
                else:
                    w, h = size
                buf = ctypes.create_string_buffer(h * w * 3)
                # Use ctypes.memmove to blit the Avisynth VFB line-by-line
                read_addr = ctypes.addressof(self.pBits.contents) + (h - 1) * self.display_pitch
                write_addr = ctypes.addressof(buf)
                P_UBYTE = ctypes.POINTER(ctypes.c_ubyte)
                for i in range(h):
                    read_ptr = ctypes.cast(read_addr, P_UBYTE)
                    write_ptr = ctypes.cast(write_addr, P_UBYTE)
                    ctypes.memmove(write_ptr, read_ptr, w * 3)
                    read_addr -= self.display_pitch
                    write_addr += w * 3
                bmp = wx.BitmapFromBuffer(w, h, buf)
                dc.DrawBitmap(bmp, 0, 0)
                return True


if __name__ == '__main__':
    AVI = AvsClip('Version().ConvertToYV12()', 'example.avs')
    if AVI.initialized:
        print('Width =', AVI.Width)
        print('Height =', AVI.Height)
        print('Framecount =', AVI.Framecount)
        print('Framerate =', AVI.Framerate)
        print('FramerateNumerator =', AVI.FramerateNumerator)
        print('FramerateDenominator =', AVI.FramerateDenominator)
        print('Audiorate =', AVI.Audiorate)
        print('Audiolength =', AVI.Audiolength)
        #~ print('AudiolengthF =', AVI.AudiolengthF)
        print('Audiochannels =', AVI.Audiochannels)
        print('Audiobits =', AVI.Audiobits)
        print('IsAudioFloat =', AVI.IsAudioFloat)
        print('IsAudioInt =', AVI.IsAudioInt)
        print('Colorspace =', AVI.Colorspace)
        print('IsRGB =', AVI.IsRGB)
        print('IsRGB24 =', AVI.IsRGB24)
        print('IsRGB32 =', AVI.IsRGB32)
        print('IsYUV =', AVI.IsYUV)
        print('IsYUY2 =', AVI.IsYUY2)
        print('IsYV24 =', AVI.IsYV24)
        print('IsYV16 =', AVI.IsYV16)
        print('IsYV12 =', AVI.IsYV12)
        print('IsYV411 =', AVI.IsYV411)
        print('IsY8 =', AVI.IsY8)
        print('IsPlanar =', AVI.IsPlanar)
        print('IsInterleaved =', AVI.IsInterleaved)
        print('IsFieldBased =', AVI.IsFieldBased)
        print('IsFrameBased =', AVI.IsFrameBased)
        print('GetParity =', AVI.GetParity)
        print('HasAudio =', AVI.HasAudio)
        print('HasVideo =', AVI.HasVideo)
    else:
        print(AVI.error_message)
    AVI = None

    AVI = AvsClip('Blackness()', 'test.avs')
    if AVI.initialized:
        print(AVI.Width)
    else:
        print(AVI.error_message)
    AVI = None

    script = """Version().ConvertToYV12()
    Sharpen(1.0)
    FlipVertical()
    """
    env = avisynth.AVS_ScriptEnvironment(3)
    try:
        clip = env.invoke('Eval', script)
    except avisynth.AvisynthError as err:
        print(err)
    else:
        if isinstance(clip, avisynth.AVS_Clip):
            AVI = AvsClip(clip, env=env)
            AVI._GetFrame(100)
            AVI = None
        else:
            print(clip.get_value())
    env = None

    print("Exit program.")

