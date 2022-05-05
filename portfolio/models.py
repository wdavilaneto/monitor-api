from django.db import models

class Board(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.CharField(max_length=200, unique=True, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    last_update = models.DateTimeField(auto_now=True, blank=True)
    hide = models.BooleanField(default=False, blank=True)
    description = models.TextField(null=True, blank=True)
    show_okr = models.BooleanField(default=False, blank=True)

    # def __init__(self, id, name):
    #     self.sid = id
    #     self.name = name

    def __repr__(self):
        return '<Board {}>'.format(self.name)

    def __str__(self):
        return '<Board {}, {}>'.format(self.sid, self.name)

    class Meta:
        ordering = ['name']
        # db_table = "board"


class Task(models.Model):
    id = models.AutoField(primary_key=True)

    trello_id = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    label = models.CharField(max_length=200)
    cycle_time = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    lead_time = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    created = models.DateField(auto_now=True, blank=True)
    start = models.DateField(auto_now=True, blank=True)
    end = models.DateField(auto_now=True, blank=True)
    friday = models.DateField(auto_now=True, blank=True)
    card_url = models.CharField(max_length=300)

    # board = models.CharField(max_length=200,null=True, blank=True)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __repr__(self):
        return '<Task {}, {}>'.format(self.trello_id, self.name)

    def __str__(self):
        return '<Task {}, {}>'.format(self.trello_id, self.name)

    class Meta:
        ordering = ['-friday', 'name']
        # db_table = "task"


# class Team(models.Model):

class Objective(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=2000, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    pain = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    risks = models.TextField(null=True, blank=True)
    quarterly = models.PositiveSmallIntegerField(default=0, null=False, blank=True)
    year = models.PositiveSmallIntegerField(default=2021, null=False, blank=True)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, related_name='objectives')

    def __repr__(self):
        return '<Objective: Q{}, {}>'.format(str(self.quarterly) + "/" + str(self.year), self.title)

    def __str__(self):
        return '<Objective: Q{}, {}>'.format(str(self.quarterly) + "/" + str(self.year), self.title)

    class Meta:
        ordering = ['-year', '-quarterly', 'text']


class KeyResults(models.Model):
    id = models.AutoField(primary_key=True)
    # acronym = models.CharField(max_length=6, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    objective = models.ForeignKey(Objective, on_delete=models.SET_NULL, null=True, blank=True, related_name='results')

    def __repr__(self):
        return '<KR: Q{}, {}>'.format(str(self.objective.quarterly) + "/" + str(self.objective.year), self.text)

    def __str__(self):
        return '<KR: Q{}, {}>'.format(str(self.objective.quarterly) + "/" + str(self.objective.year), self.text)


class KeyResultValue(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=True, blank=True)
    month = models.PositiveSmallIntegerField(default=1, null=False, blank=True)
    value1 = models.PositiveSmallIntegerField(default=0, null=False, blank=True)
    value2 = models.PositiveSmallIntegerField(default=0, null=False, blank=True)
    value3 = models.PositiveSmallIntegerField(default=0, null=False, blank=True)
    value4 = models.PositiveSmallIntegerField(default=0, null=False, blank=True)
    final = models.PositiveSmallIntegerField(default=0, null=False, blank=True)

    kr = models.ForeignKey(KeyResults, on_delete=models.SET_NULL, null=True, blank=True, related_name='values')

    def __repr__(self):
        return '<KR: M{}, {}>'.format(str(self.month) + "/" + str(self.id), self.kr.text)

    def __str__(self):
        return '<KR: M{}, {}>'.format(str(self.month) + "/" + str(self.id), self.kr.text)

    class Meta:
        ordering = ['month']
