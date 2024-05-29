.PHONY: clean

testfloat_gen := /home/yanson/Git/CoqValidationIEEE754/regression/TestFloat-3e/build/Linux-x86_64-GCC/testfloat_gen
# testfloat_gen := /home/yanson/Git/FlocqValidationIEEE754/regression/TestFloat-3e/build/Linux-x86_64-GCC/testfloat_gen

rounding := rnear_even rnear_maxMag rminMag rmin rmax 
n := 


# USAGE: make testfloat format="f32"/"f64" level="1"/"2"
testfloat: $(rounding)

$(rounding): 
	mkdir -p testfloat_tests/testfloat_$(format)_level$(level)/$@
	$(testfloat_gen) -level $(level) $(n) -$@ $(format)_add > testfloat_tests/testfloat_$(format)_level$(level)/$@/$(format)_add.txt
	$(testfloat_gen) -level $(level) $(n) -$@ $(format)_sub > testfloat_tests/testfloat_$(format)_level$(level)/$@/$(format)_sub.txt
	$(testfloat_gen) -level $(level) $(n) -$@ $(format)_mul > testfloat_tests/testfloat_$(format)_level$(level)/$@/$(format)_mul.txt
	$(testfloat_gen) -level $(level) $(n) -$@ $(format)_div > testfloat_tests/testfloat_$(format)_level$(level)/$@/$(format)_div.txt
	$(testfloat_gen) -level $(level) $(n) -$@ $(format)_sqrt > testfloat_tests/testfloat_$(format)_level$(level)/$@/$(format)_sqrt.txt
	# $(testfloat_gen) -level $(level) $(n) -$@ $(format)_mulAdd > testfloat_tests/testfloat_$(format)_level$(level)/$@/$(format)_mulAdd.txt

testfloat_fma:
	mkdir -p testfloat_tests/testfloat_fma_$(format)
	$(testfloat_gen) -level 1 -rnear_even $(format)_mulAdd > testfloat_tests/testfloat_fma_$(format)/rnear_even_$(format)_mulAdd.txt
	$(testfloat_gen) -level 1 -rnear_maxMag $(format)_mulAdd > testfloat_tests/testfloat_fma_$(format)/rnear_maxMag_$(format)_mulAdd.txt
	$(testfloat_gen) -level 1 -rminMag $(format)_mulAdd > testfloat_tests/testfloat_fma_$(format)/rminMag_$(format)_mulAdd.txt
	$(testfloat_gen) -level 1 -rmin $(format)_mulAdd > testfloat_tests/testfloat_fma_$(format)/rmin_$(format)_mulAdd.txt
	$(testfloat_gen) -level 1 -rmax $(format)_mulAdd > testfloat_tests/testfloat_fma_$(format)/rmax_$(format)_mulAdd.txt

run_fma:
	python runner_test_float.py $(format) testfloat_tests/testfloat_fma_f32/rmax_$(format)_mulAdd.txt mulAdd rmax false
	python runner_test_float.py $(format) testfloat_tests/testfloat_fma_f32/rmin_$(format)_mulAdd.txt mulAdd rmin false
	python runner_test_float.py $(format) testfloat_tests/testfloat_fma_f32/rminMag_$(format)_mulAdd.txt mulAdd rminMag false
	python runner_test_float.py $(format) testfloat_tests/testfloat_fma_f32/rnear_maxMag_$(format)_mulAdd.txt mulAdd rnear_maxMag false
	python runner_test_float.py $(format) testfloat_tests/testfloat_fma_f32/rnear_even_$(format)_mulAdd.txt mulAdd rnear_even false

clean: 
	rm -rf __pycache__ testfloat__level
	rm -f tmp.glob tmp.v tmp.vo tmp.vok tmp.vos .tmp.aux

run_testfloat:
	mkdir -p testfloat_results
	./RunTestFloatTests.sh testfloat_tests/testfloat_$(format)_level$(level)/rnear_even rnear_even > testfloat_results/rnear_even_$(format)_level$(level).txt
	./RunTestFloatTests.sh testfloat_tests/testfloat_$(format)_level$(level)/rnear_maxMag rnear_maxMag > testfloat_results/rnear_maxMag_$(format)_level$(level).txt
	./RunTestFloatTests.sh testfloat_tests/testfloat_$(format)_level$(level)/rminMag rminMag > testfloat_results/rminMag_$(format)_level$(level).txt
	./RunTestFloatTests.sh testfloat_tests/testfloat_$(format)_level$(level)/rmin rmin > testfloat_results/rmin_$(format)_level$(level).txt
	./RunTestFloatTests.sh testfloat_tests/testfloat_$(format)_level$(level)/rmax rmax > testfloat_results/rmax_$(format)_level$(level).txt

gen_benchmark:
	mkdir -p testfloat_tests/benchmark/rnear_even/$(format)
	$(testfloat_gen) -level 1 -rnear_even -n 1000000 $(format)_add > testfloat_tests/benchmark/rnear_even/$(format)/$(format)_add.txt
	$(testfloat_gen) -level 1 -rnear_even -n 1000000 $(format)_sub > testfloat_tests/benchmark/rnear_even/$(format)/$(format)_sub.txt
	$(testfloat_gen) -level 1 -rnear_even -n 1000000 $(format)_mul > testfloat_tests/benchmark/rnear_even/$(format)/$(format)_mul.txt
	$(testfloat_gen) -level 1 -rnear_even -n 1000000 $(format)_div > testfloat_tests/benchmark/rnear_even/$(format)/$(format)_div.txt
	$(testfloat_gen) -level 1 -rnear_even -n 1000000 $(format)_sqrt > testfloat_tests/benchmark/rnear_even/$(format)/$(format)_sqrt.txt
	# MUST BE CREATED MANUALLY: testfloat_tests/benchmark/rnear_even/$(format)/$(format)_mulAdd.txt (eg. by cutting and pasting 1 000 000 test vectors for mulAdd rnear_even to a text file)


# USAGE: make run_benchmark format="f32"
#        make run_benchmark format="f64"
run_benchmark:
	mkdir -p testfloat_results
	./RunTestFloatTests.sh testfloat_tests/benchmark/rnear_even/$(format) rnear_even > testfloat_results/benchmark_rnear_even_$(format).txt