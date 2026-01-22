from PyBitStat import even_only, even_stats, sign_counts, median_even, format_even_stats, to_binary_divmod, save_even_report, count_ones, is_power_of_two, count_ones_fast, parity, highest_bit_index, is_kth_bit_set, clear_kth_bit, set_kth_bit, toggle_kth_bit, _check_non_negative_int
import inspect

def pp(name, got, expect):
    ok = (got == expect)
    print(f"{name}: {'OK' if ok else 'FAIL'} got={got}  expect={expect}")

# ---- even_only ----
pp("eo_1", even_only([1, 2, 3, 4]), [2, 4])
pp("eo_2", even_only([1.0, 2.0, 3.5, True, "7"]), [2])
pp("eo_3", even_only([-4, -3, 0, 5]), [-4, 0])

# ---- even_stats ----
pp("es_1", even_stats([1, 2, 3, 4]), {'sum': 6, 'min': 2, 'max': 4, 'avg': 3.0})
pp("es_2", even_stats([1, 3, 5]), None)
print("\nhelp(even_stats):")
print(inspect.getdoc(even_stats))

# ---- sign_counts ----
pp("sc_1", sign_counts([-2, -1, 0, 1, 2]), {'pos': 2, 'neg': 2, 'zero': 1})
pp("sc_2", sign_counts([True, False, 0.0, -3.0, "x", 4.0]), {'pos': 1, 'neg': 1, 'zero': 1})

# ---- median_even ----
pp("me_1", median_even([1.0, 2.0, 3.5, True, "7"]), 2)
pp("me_2", median_even([-4, -2, 0, 2]), -1.0)

# ---- format_even_stats ----
"""
Кратко что делает...
    >>> format_even_stats([1, 2, 3, 4])
    sum=6, min=2, max=4, avg=3.0
    >>> format_even_stats([1, 3, 5])
    нет чётных чисел.
    >>> format_even_stats([1.0, 2.0, 3.5, True, "7"])
    sum=2, min=2, max=2, avg=2.0
    """
pp("fes_1", format_even_stats([1, 2, 3, 4]), "sum=6, min=2, max=4, avg=3.0")
pp("fes_2", format_even_stats([1, 3, 5]), "нет чётных чисел")
pp("fes_3", format_even_stats([1.0, 2.0, 3.5, True, "7"]), "sum=2, min=2, max=2, avg=2.0")
pp("fes_none", format_even_stats([1, 3, 5]), "нет чётных чисел")


# ---- to_binary_divmod ----
pp("tb_1", to_binary_divmod(0), "0")
pp("tb_2", to_binary_divmod(37), "100101")
pp("tb_3", to_binary_divmod(26), "11010")
pp("tb_4", to_binary_divmod(73), "1001001")
pp("tb_5", to_binary_divmod(255), "11111111")
ok = False
try:
    to_binary_divmod('10')
except:
    ok = True
pp("tb_bad_1", ok, True)

# ---- save_even_report ----
ok = save_even_report([1, 2, 3, 4], "rep1.txt", "txt")
with open("rep1.txt", "r", encoding="utf-8") as f:
    txt = f.read()
pp("sr_txt1", (ok, txt), (True, "sum=6, min=2, max=4, avg=3.0\n"))

import os
p = os.path.abspath("rep2.csv")        
ok_csv = save_even_report([1,2,3,4], p, "csv")
pp("exists_csv", os.path.exists(p), True)
with open(p, "r", encoding="utf-8") as f:
    csvtxt = f.read()
pp("sr_csv1", (ok_csv, csvtxt), (True, "sum,min,max,avg\n6,2,4,3.0\n"))

ok = save_even_report([1, 3, 5], "rep_empty.txt", "txt")
with open("rep_empty.txt", "r", encoding="utf-8") as f:
    txt = f.read()
pp("sr_txt_empty", (ok, txt), (True, "нет чётных целых\n"))

ok = False
try:
    save_even_report([1, 2], "bad.txt", "pdf")
except ValueError:
    ok = True
pp("sr_bad_fmt", ok, True)

ok = save_even_report([1, 3, 5], "rep_empty.csv", "csv")
with open("rep_empty.csv", "r", encoding="utf-8") as f:
    txt = f.read()
pp("sr_csv_empty", (ok, txt), (True, "sum,min,max,avg\n"))


# ---- count_ones ----
pp("co_0", count_ones(0), 0)
pp("co_7", count_ones(7), 3)
pp("co_8", count_ones(8), 1)
pp("co_255", count_ones(255), 8)
pp("co_1023", count_ones(1023), 10)

# ---- is_power_of_two ----
pp("pow2_0", is_power_of_two(0), False)
pp("pow2_1", is_power_of_two(1), True)
pp("pow2_1024", is_power_of_two(1024), True)
pp("pow2_1023", is_power_of_two(1023), False)

# ---- count_ones_fast ----
pp("cof_0", count_ones_fast(0), 0)
pp("cof_1", count_ones_fast(1), 1)
pp("cof_8", count_ones_fast(8), 1)
pp("cof_1023", count_ones_fast(1023), 10)
pp("cof_1024", count_ones_fast(1024), 1)
pp("cof_eq_1023", count_ones_fast(1023), count_ones(1023))

# ---- parity ----
pp("p_0", parity(0), False)
pp("p_1", parity(1), True)
pp("p_8", parity(8), True)
pp("p_1023", parity(1023), False)
pp("p_1024", parity(1024), True)
pp("p_1022", parity(1022), True)
pp("parity_aa", parity(0b10101010), False)
pp("parity_ab", parity(0b10101011), True)
try: 
    parity(-1)
    pp('p_bad', 'no-exc', 'ValueError')
except ValueError:
    pp("p_bad", 'ValueError', 'ValueError')

# ---- highest_bit_index ----
pp("hbi_0", highest_bit_index(0), None)
pp("hbi_1", highest_bit_index(1), 0)
pp("hni_8", highest_bit_index(8), 3)
pp("hbi_1023", highest_bit_index(1023), 9)

# ---- is_kth_bit_set ----
pp("bit_22_0", is_kth_bit_set(22, 0), False)
pp("bit_22_4", is_kth_bit_set(22, 4), True)
try:
    is_kth_bit_set(-1, 0)
    pp("bit_n_neg", "no-exc", "ValueError")

except ValueError:
    pp("bit_n_neg", "ValueError", "ValueError")

try:
    is_kth_bit_set(22, -1)
    pp("bit_k_neg", "no-exc", "ValueError")
except ValueError:
    pp("bit_k_neg", "ValueError", "ValueError")

try:
    is_kth_bit_set("22", 1)
    pp("bit_n_type", "no-exc", "TypeError")
except TypeError:
    pp("bit_n_type", "TypeError", "TypeError")
    
try:
    is_kth_bit_set(22, "1")
    pp("bit_k_type", "no-exc", "TypeError")
except TypeError:
    pp("bit_k_type", "TypeError", "TypeError")

# ---- clear_kth_bit ----
pp("clr_22_1", clear_kth_bit(22, 1), 20)
pp("clr_22_2", clear_kth_bit(22, 2), 18)
pp("clr_bigk", clear_kth_bit(22, 10), 22)
pp("clr_22_4", clear_kth_bit(22, 4), 6)
pp("clr_idempotent_20_0", clear_kth_bit(clear_kth_bit(22, 4), 4), clear_kth_bit(22, 4))
pp("clr_after_set_eq", clear_kth_bit(set_kth_bit(22, 4), 4), clear_kth_bit(22, 4))
try:
    clear_kth_bit(-1, 0)
    pp("clr_n_neg", "no-exc", "ValueError")
except ValueError:
    pp("clr_n_neg", "ValueError", "ValueError")

try:
    clear_kth_bit(22, -1)
    pp("clr_k_neg", "no-exc", "ValueError")
except ValueError:
    pp("clr_k_neg", "ValueError", "ValueError")

try:
    clear_kth_bit("22", 1)
    pp("clr_n_type", "no-exc", "ValueError")
except TypeError:
    pp("clr_n_type", "TypeError", "TypeError")

try:
    clear_kth_bit(22, "1")
    pp("clr_k_type", "no_exc", "TypeError")
except TypeError:
    pp("clr_k_type", "TypeError", "TypeError")

# ---- set_kth_bit ----
pp("set_1", set_kth_bit(22, 0), 23)
pp("set_idem", set_kth_bit(22, 1), 22)
pp("set_high", set_kth_bit(0, 5), 32)
pp("set_idempotent_20_0", set_kth_bit(set_kth_bit(20, 0), 0), set_kth_bit(20, 0))
pp("set_after_clear_eq", set_kth_bit(clear_kth_bit(20, 0), 0), set_kth_bit(20, 0))
try:
    set_kth_bit(-1, 1); pp("set_n_neg", "no_exc", "ValueError")
except ValueError:
    pp("set_n_neg", "ValueError", "ValueError")

try:
    set_kth_bit(5, -1); pp("set_k_neg", "no_exc", "ValueError")
except ValueError: 
    pp("set_k_neg", "ValueError", "ValueError")

try:
    set_kth_bit(True, 1); pp("set_n_bool", "no_exc", "TypeError")
except TypeError:
    pp("set_n_bool", "TypeError", "TypeError")

# ---- toggle_kth_bit ----
pp("tog_22_0", toggle_kth_bit(22, 0), 23)
pp("tog_22_1", toggle_kth_bit(22, 1), 20)
pp("tog_twice", toggle_kth_bit(toggle_kth_bit(22, 1), 1), 22)
pp("tog_high", toggle_kth_bit(0, 5), 32)
pp("tog_involution_22_4", toggle_kth_bit(toggle_kth_bit(22, 4), 4), 22)
try:
    toggle_kth_bit(5, -1); pp("tog_k_neg", "no_exc", "ValueError")
except ValueError:
    pp("tog_k_neg", "ValueError", "ValueError")

try:
    toggle_kth_bit(True, 0); pp("tog_n_bool", "no_exc", "TypeError")
except TypeError:
    pp("tog_n_bool", "TypeError", "TypeError")

# ---- doctest ----
import doctest, PyBitStat
pp("doctest_failed", doctest.testmod(PyBitStat).failed, 0)

