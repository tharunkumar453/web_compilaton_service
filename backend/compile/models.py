from django.db import models

class problem_table(models.Model):
	problem_id=models.SlugField(max_length=20,null=False,unique=True,primary_key=True)
	Problem_discription=models.TextField(null=True,blank=True)
	test_cases=models.FileField(upload_to="testcase/",null=False)

	def __str__ (self):
		return f"PROBLEM_ID:-{self.problem_id} || PROBLEM_DESCRIPTION:-{self.Problem_discription}"
	

class UserBoard(models.Model):
	email=models.EmailField(blank=False)
	problem=models.ForeignKey(problem_table, on_delete=models.CASCADE, blank=True, null=True,to_field=problem_table().problem_id ,related_name="userboards")
	has_done=models.BooleanField(default=False)
	language_used=models.CharField(max_length=20,blank=False)
	time_of_submission=models.TimeField(auto_now_add=True)

	def __str__(self):
		return f"EMAIL:-{self.email} || PROBLEM_ID:-{self.problem} || LANGUAGE:-{self.language_used} || STATUS:-{self.has_done} || TIME:-{self.time_of_submission}"

class submission(models.Model):
	email=models.EmailField(blank=False)
	submission_id=models.SlugField(max_length=20,unique=True,serialize=False)
	problem=models.ForeignKey(problem_table, on_delete=models.CASCADE, blank=True, null=True,to_field=problem_table().problem_id ,related_name="submissions")
	language_used=models.CharField(max_length=20,blank=False)
	time_of_submission=models.TimeField(auto_now_add=True)
	code_file = models.FileField(upload_to="submissions/",null=False)
	def __str__(self):
		return f"EMAIL:-{self.email} || PROBLEM_ID:-{self.problem} || SUBMISSION_ID:-{self.submission_id} || TIME:-{self.time_of_submission}"