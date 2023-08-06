
# PRE Workbench
# Copyright (C) 2022 Mira Weller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct

from PyQt5.QtGui import QColor, QPen, QPainter

from pre_workbench.objects import ByteBuffer


def extendRange(bbuf, range, amount=16):
	(selMin, selMax) = range
	return max(0, selMin - amount), min(bbuf.length, selMax + amount)

def rangeBefore(bbuf, range, amount=16):
	(selMin, selMax) = range
	return max(0, selMin - amount), selMin

def intToVarious(*values):
	for value in values:
		if value < 0:
			yield from intToFmts(value, [">q","<q",">i","<i",">h","<h",">b","<b"])
		else:
			yield from intToFmts(value, [">Q","<Q",">I","<I",">H","<H",">B","<B"])
		yield str(value).encode("utf-8"), "d"
		yield ("%x"%value).encode("utf-8"), "x"
		yield ("%X"%value).encode("utf-8"), "X"


def intToFmts(value, fmts):
	for fmt in fmts:
		try:
			yield struct.pack(fmt, value), fmt
		except struct.error:
			pass

def findInRange(bbuf, ranges, values):
	for (start, end) in ranges:
		for val, desc in values:
			l = len(val)
			for i in range(start, end-l+1):
				if bbuf.buffer[i:i+l] == val:
					yield (i, i+l), desc

def highlightMatch(editor, qp: QPainter, matchrange, desc, color):
	(start,end)=matchrange
	for i in range(start,end):
		(xHex, xAscii, y, dy) = editor.offsetToClientPos(i)
		if dy is None: break
		p = QPen(color)
		p.setWidth(3)
		qp.setPen(p)
		qp.drawLine(xHex+3, y+dy+1, xHex+editor.dxHex-3, y+dy+1)
		qp.drawLine(xAscii+1, y+dy+1, xAscii+editor.dxAscii-2, y+dy+1)


def selectionLengthMatcher(editor, qp, bbuf, sel):
	(start, end) = sel
	sellen = end - start + 1
	if sellen == 0: return
	for match, desc in findInRange(bbuf, [extendRange(bbuf, (start,start))], intToVarious(sellen)):
		highlightMatch(editor, qp, match,desc,QColor("#ff00ff"))
	for match, desc in findInRange(bbuf, [extendRange(bbuf, (start,start))], intToVarious(sellen+1, sellen+2, sellen+4)):
		highlightMatch(editor, qp, match,desc,QColor("#993399"))

def debug_highlightMatchRange(editor, qp, bbuf, sel):
	highlightMatch(editor, qp, rangeBefore(bbuf, sel), "", QColor("#555555"))

def highlightSelectionAsLength(editor, qp, bbuf:ByteBuffer, sel):
	(start, end)=sel
	end=end+1
	if end-start>8: return
	val = bbuf.getInt(start,end,endianness=">",signed=False)
	if val > 0 and end+val < len(bbuf):
		highlightMatch(editor, qp, (end, end+val), "", QColor("#555555"))
		return
	val = bbuf.getInt(start,end,endianness="<",signed=False)
	if val > 0 and end+val < len(bbuf):
		highlightMatch(editor, qp, (end, end+val), "", QColor("#555555"))
		return

def highlightRepetitions(editor, qp, bbuf, sel):
	(start, end) = sel
	sellen = end - start + 1
	if sellen == 0: return
	for match, desc in findInRange(bbuf, [editor.visibleRange()], [(bbuf.getBytes(start, sellen), "")]):
		highlightMatch(editor, qp, match, desc, QColor("#009999"))

selectionHelpers = [
	#debug_highlightMatchRange,
	highlightSelectionAsLength,
	selectionLengthMatcher,
	highlightRepetitions,
]
