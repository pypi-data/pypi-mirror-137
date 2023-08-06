# -*- coding: utf-8 -*-
import copy
import re
from collections.abc import Iterable
from json import JSONDecodeError

import pandas as pd

from . import hit_api_io
from .course_mask import CourseMask


class CourseSet:
    cols = ['上课地点', '教师', '课程名', '周次', '上课时间', '星期']

    def __init__(self, course, week=None, semester=None):
        """

        :param courses:
        :param week:
        """
        if not isinstance(course, pd.DataFrame):
            course = self.__week_courses_to_df(course)
        self.course_table = course
        self.course_table.drop_duplicates(inplace=True)
        self.week = week
        self.semester = semester

    @property
    def mask(self):
        return CourseMask.fromCourseSet(self)

    @staticmethod
    def __week_courses_to_df(interest) -> pd.DataFrame:
        """

        :param interest:
        :return:
        """
        res = pd.DataFrame(interest)
        col = ['上课地点', '教师', '课程名', '周次', '_', '上课时间', '星期', '__']
        try:
            res.columns = col
        except ValueError:
            res = pd.DataFrame(columns=col)
        res.drop(columns='_', inplace=True)
        res.drop(columns='__', inplace=True)
        return res

    @staticmethod
    def fromIteratorSearch(week, semester, course_name: str = None, it=None):
        if it is None:
            def _generate_id():
                prefix = '120L'
                suffix = '01'
                for i in range(1, 5):
                    for j in range(1, 20):
                        yield prefix + str(i).zfill(2) + str(j).zfill(2) + suffix

            it = _generate_id()
        res = []
        for iter_result in hit_api_io.from_iterable(it, week, semester):
            try:
                courses = iter_result.json()['module']['data']
                for course in courses:
                    name = str(course['kcmc'])
                    if course_name is None or name.find(course_name) != -1:
                        res.append(course)
            except JSONDecodeError:
                # 可能出现了本不应该出现的学号，应该跳过
                continue
        return CourseSet(res, week, semester)

    def fromOtherSet(self, other, week=None, semester=None):
        """

        :param other:
        :return:
        """
        if semester is None:
            semester = self.semester
        if week is None:
            week = self.week    
        if not isinstance(other, CourseSet):
            
            if isinstance(other, str):
                other_set = CourseSet.fromPerson(other, week, semester)
            elif isinstance(other, Iterable):
                other_set = CourseSet.fromIteratorSearch(week, semester, None, other)
            else:
                raise ValueError("Cannot subtract from this")
        else:
            other_set = other
        return other_set

    @staticmethod
    def fromPerson(hit_id, week: int, semester: str):
        return CourseSet.fromIteratorSearch(week, it=[hit_id], semester=semester)

    @staticmethod
    def fromPickle(filepath, week: int=None, semester: str=None):
        """

        :return:
        """
        data = pd.read_pickle(filepath)
        return CourseSet(data, week, semester)

    @classmethod
    def fromEmpty(cls, week=None, semester=None):
        return CourseSet(pd.DataFrame(columns=cls.cols), week, semester)

    def toPickle(self, io):
        self.course_table.to_pickle(io)

    def filterFromMask(self, mask: CourseMask, inplace=True):
        del_indexes = []
        if inplace:
            t = self.course_table
        else:
            t = copy.deepcopy(self.course_table)
        for index, course in self.course_table.iterrows():
            if not mask.checkCourse(course):
                del_indexes.append(index)
        self.course_table.drop(index=del_indexes, inplace=True)
        if not inplace:
            return CourseSet(t, self.week, self.semester)
        else:
            return self

    def toExcel(self, io):
        """

        :param io:
        :return:
        """
        self.course_table.to_excel(io, index=False)

    @classmethod
    def fromExcel(cls, io, week=None, semester=None):
        courses = pd.read_excel(io)
        return cls(courses, week, semester)

    def filterFromStr(self, r, inplace=True):
        pattern = re.compile(r)
        indexes = []
        for index, course in self.course_table.iterrows():
            indexes.append(index) if pattern.match(course['课程名']) else None
        if inplace:
            self.course_table = self.course_table.loc[indexes]
            return self
        else:
            p = copy.deepcopy(self.course_table.loc[indexes])
            return CourseSet(p, self.week, self.semester)

    def __and__(self, other):
        """

        :param other:
        :return:
        """
        other_set = self.fromOtherSet(other)
        other_mask = CourseMask.fromCourseSet(other_set)
        return self.filterFromMask(other_mask, inplace=False)

    def __sub__(self, other):
        other_set = self.fromOtherSet(other)
        other_mask = CourseMask.fromCourseSet(other_set)
        return self.filterFromMask(~other_mask, inplace=False)

    def __str__(self):
        return str(self.course_table)

    def __add__(self, other):
        other_set = self.fromOtherSet(other)
        return CourseSet(self.course_table.append(other_set.course_table, ignore_index=True))
