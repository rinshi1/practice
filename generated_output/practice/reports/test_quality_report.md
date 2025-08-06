# Test Generation Quality Report
    
**Agent:** practice  
**Generated:** 2025-08-06 12:19:26  
**Status:** ❌ FAILED

---

## 📊 Executive Summary


| Metric | Value | Status |
|--------|-------|--------|
| **Test Coverage** | 0.0% | ❌ |
| **Code Quality Score** | 0/100 | ❌ |
| **Functions Analyzed** | 2 | ✅ |
| **Classes Analyzed** | 1 | ✅ |
| **Tests Passed** | 0/0 | ❌ |
| **Total Statements** | 112 | ✅ |
| **Covered Statements** | 0 | ⚠️ |


---

## 🧪 Test Results


### Test Execution Summary
- **Total Tests:** 0
- **Passed:** 0 ✅
- **Failed:** 0 ❌
- **Skipped:** 0 ⏭️
- **Success Rate:** 0.0%
- **Duration:** 14.76s

### Test Status
⚠️ No tests executed


---

## 📈 Code Coverage Analysis


### Coverage Summary
- **Overall Coverage:** 0.0% ❌
- **Total Statements:** 112
- **Covered Statements:** 0
- **Missing Statements:** 112
- **Coverage Threshold:** 80%
- **Status:** Below threshold

### File Coverage Details

| File | Statements | Missing | Coverage | Status |
|------|------------|---------|----------|--------|
| `test_integration_agent.py` | 62 | 62 | 0.0% | ❌ |
| `test_unit_agent.py` | 50 | 50 | 0.0% | ❌ |


### Missing Coverage Analysis
- **test_integration_agent.py:** Lines 2, 3, 4, 5, 6, 7, 8, 9, 10, 11... (62 total)
- **test_unit_agent.py:** Lines 2, 3, 4, 5, 6, 7, 8, 9, 11, 12... (50 total)

### Coverage Reports
- **HTML Report:** Available in `coverage/htmlcov/index.html`
- **JSON Report:** Available in `coverage/coverage.json`
- **XML Report:** Available in `coverage/coverage.xml`


---

## 🔍 Static Analysis


### Static Analysis Summary
- **Quality Score:** 0/100 ❌
- **Total Issues:** 110
- **Tools Success Rate:** 3/4

### Issue Breakdown
- **Errors:** 4 ❌
- **Warnings:** 36 ⚠️
- **Security Issues:** 0 🔒
- **Info/Style:** 70 ℹ️

### Tool Results
- **Ruff:** 27 issues ❌
- **Mypy:** Failed (Timeout) ❌
- **Bandit:** 0 issues ✅
- **Pylint:** 83 issues ❌


---

## 📋 Code Structure Analysis


### Code Structure
- **Functions:** 2
- **Classes:** 1
- **Imports:** 13



---

## 🎯 Recommendations

1. 🎯 Increase test coverage from 0.0% to at least 80%
2. 📁 Focus on improving coverage in: test_integration_agent.py, test_unit_agent.py
3. 📝 Add tests for 112 uncovered statements
4. 📋 Fix type errors and critical issues
5. 📋 Consider addressing style and convention warnings
6. 📋 Code quality is below acceptable threshold (70)
7. ⚡ Improve code quality to meet minimum standards

---

## 📄 Detailed Results

### Test Execution Details
```json
{
  "total": 0,
  "passed": 0,
  "failed": 0,
  "skipped": 0,
  "duration": 14.759571552276611,
  "exit_code": 2,
  "details": {
    "created": 1754462917.6768448,
    "duration": 14.759571552276611,
    "exitcode": 2,
    "root": "D:\\OneDrive - Olam International\\Desktop\\Test_Suite_Generator_agent",
    "environment": {},
    "summary": {
      "total": 0,
      "collected": 7
    },
    "collectors": [
      {
        "nodeid": "",
        "outcome": "passed",
        "result": [
          {
            "nodeid": "practice/output/tests",
            "type": "Dir"
          }
        ]
      },
      {
        "nodeid": "practice/output/tests/test_integration_agent.py",
        "outcome": "failed",
        "result": [],
        "longrepr": "ImportError while importing test module 'D:\\OneDrive - Olam International\\Desktop\\Test_Suite_Generator_agent\\practice\\output\\tests\\test_integration_agent.py'.\nHint: make sure your test modules/packages have valid Python names.\nTraceback:\nC:\\Users\\rinshi.kumari\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\importlib\\__init__.py:90: in import_module\n    return _bootstrap._gcd_import(name[level:], package, level)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\npractice\\output\\tests\\test_integration_agent.py:13: in <module>\n    from langgraph.schema import HumanMessage, SystemMessage\nE   ModuleNotFoundError: No module named 'langgraph.schema'"
      },
      {
        "nodeid": "practice/output/tests/test_unit_agent.py",
        "outcome": "passed",
        "result": [
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_chatbot_happy_path",
            "type": "Function",
            "lineno": 16
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_chat_happy_path",
            "type": "Function",
            "lineno": 25
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_chat_empty_user_input",
            "type": "Function",
            "lineno": 36
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_chat_error_handling",
            "type": "Function",
            "lineno": 47
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_environment_variables",
            "type": "Function",
            "lineno": 58
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_chat_multiple_inputs[I want to book a flight to New York.-Booking confirmed!]",
            "type": "Function",
            "lineno": 74
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py::test_chat_multiple_inputs[Can you find me tickets to London?-Booking confirmed!]",
            "type": "Function",
            "lineno": 74
          }
        ]
      },
      {
        "nodeid": "practice/output/tests",
        "outcome": "passed",
        "result": [
          {
            "nodeid": "practice/output/tests/test_integration_agent.py",
            "type": "Module"
          },
          {
            "nodeid": "practice/output/tests/test_unit_agent.py",
            "type": "Module"
          }
        ]
      }
    ],
    "tests": [],
    "warnings": [
      {
        "message": "websockets.legacy is deprecated; see https://websockets.readthedocs.io/en/stable/howto/upgrade.html for upgrade instructions",
        "category": "DeprecationWarning",
        "when": "collect",
        "filename": "D:\\OneDrive - Olam International\\Desktop\\Test_Suite_Generator_agent\\myenv\\Lib\\site-packages\\websockets\\legacy\\__init__.py",
        "lineno": 6
      }
    ]
  },
  "success": true
}
```

### Coverage Details
```json
{
  "total_coverage": 0.0,
  "total_statements": 112,
  "covered_statements": 0,
  "missing_statements": 112,
  "files": {
    "practice\\output\\tests\\test_integration_agent.py": {
      "statements": 62,
      "missing": 62,
      "covered": 0,
      "coverage_percent": 0.0,
      "missing_lines": [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        26,
        27,
        28,
        29,
        30,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        41,
        42,
        50,
        51,
        53,
        54,
        55,
        56,
        57,
        59,
        60,
        61,
        63,
        64,
        65,
        66,
        68,
        69,
        70,
        72,
        73,
        74,
        75,
        76,
        77,
        79,
        81
      ],
      "excluded_lines": []
    },
    "practice\\output\\tests\\test_unit_agent.py": {
      "statements": 50,
      "missing": 50,
      "covered": 0,
      "coverage_percent": 0.0,
      "missing_lines": [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        11,
        12,
        14,
        15,
        17,
        19,
        21,
        22,
        24,
        26,
        28,
        30,
        31,
        33,
        35,
        37,
        39,
        41,
        42,
        44,
        46,
        48,
        51,
        53,
        54,
        56,
        57,
        59,
        61,
        62,
        67,
        69,
        70,
        71,
        72,
        73,
        75,
        79,
        81,
        83,
        84,
        86
      ],
      "excluded_lines": []
    }
  },
  "meta": {
    "format": 3,
    "version": "7.9.1",
    "timestamp": "2025-08-06T12:18:39.660712",
    "branch_coverage": false,
    "show_contexts": false
  },
  "totals": {
    "covered_lines": 0,
    "num_statements": 112,
    "percent_covered": 0.0,
    "percent_covered_display": "0",
    "missing_lines": 112,
    "excluded_lines": 0
  }
}
```

### Static Analysis Details
```json
{
  "total_issues": 110,
  "tools_run": 4,
  "tools_successful": 3,
  "severity_breakdown": {
    "error": 4,
    "warning": 36,
    "info": 70,
    "security": 0
  },
  "quality_score": 0,
  "recommendations": [
    "Fix type errors and critical issues",
    "Consider addressing style and convention warnings",
    "Code quality is below acceptable threshold (70)"
  ]
}
```

---

*Report generated by Test Generator Agent*
