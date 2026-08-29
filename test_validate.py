"""Tests for validate.py.

The validator is the component every measurement in this project now
depends on: the schema-violation counts in CHANGELOG.md come from it, and
agent.py's correction loop is driven by it. Nothing had ever checked that
its three rules work. This does.

Two kinds of test live here.

  Behaviour tests -- the rules catch what they should and pass what they
  should. If one of these fails, the validator is broken.

  Known-gap tests -- they assert what the validator currently does at four
  edges where it is weaker than it looks. They are written to FAIL if the
  behaviour changes, so that tightening a rule forces the documentation to
  be updated with it. Each one names the gap in its docstring.

Run it directly -- no API key, no network, no dependencies:

    python test_validate.py

It is also plain pytest-compatible if pytest happens to be installed.
"""

import sys

from validate import NUMBER, normalise, sources_from_prompt, validate_response


# --- helpers ---------------------------------------------------------------

def assertion(**overrides) -> dict:
    """One well-formed assertion, with any field overridden per test."""
    base = {
        "status": "verified",
        "quote": "Nabil declared a 12.50% cash dividend",
        "source_figure": "12.50%",
        "source_file": "nabil.md",
    }
    base.update(overrides)
    return base


def response(*assertions) -> dict:
    return {"assertions": list(assertions)}


# The source text the assertions above are checked against.
SOURCES = {"nabil.md": "For FY 2081/2082 Nabil declared a 12.50% cash dividend."}


# --- normalise -------------------------------------------------------------

def test_normalise_collapses_runs_of_whitespace():
    assert normalise("a  \n\t b") == "a b"


def test_normalise_strips_the_edges():
    assert normalise("  padded  ") == "padded"


# --- sources_from_prompt ---------------------------------------------------

def test_sources_is_empty_when_the_marker_is_absent():
    # A prompt with no source block yields no sources, rather than raising.
    assert sources_from_prompt("no markers here") == {}


def test_sources_parses_each_named_file():
    prompt = (
        "=== SOURCE DOCUMENTS ===\n"
        "--- sources/nabil.md ---\nNabil text.\n"
        "--- sources/ebl.md ---\nEBL text.\n"
        "=== CLAIM ===\nthe claim"
    )
    parsed = sources_from_prompt(prompt)
    assert parsed["sources/nabil.md"] == "Nabil text."
    assert parsed["sources/ebl.md"] == "EBL text."


def test_sources_stops_at_the_claim_marker():
    # The claim itself must never become quotable source text.
    prompt = (
        "=== SOURCE DOCUMENTS ===\n"
        "--- sources/nabil.md ---\nreal source\n"
        "=== CLAIM ===\nfabricated claim text"
    )
    assert "fabricated" not in sources_from_prompt(prompt)["sources/nabil.md"]


# --- rule 1: the status must be one the schema permits ---------------------

def test_each_permitted_status_passes():
    for status in ("verified", "contradicted", "not_found"):
        # No figure or quote, so only rule 1 is in play.
        result = validate_response(
            response({"status": status}), SOURCES
        )
        assert result == [], f"{status} should be accepted"


def test_an_invented_status_is_flagged():
    result = validate_response(response({"status": "unsupported"}), SOURCES)
    assert len(result) == 1 and "unsupported" in result[0]


def test_status_matching_is_case_sensitive():
    # "Verified" is not "verified" -- the schema names exact strings.
    result = validate_response(response({"status": "Verified"}), SOURCES)
    assert len(result) == 1


def test_a_missing_status_is_flagged():
    result = validate_response(response({"quote": "x"}), SOURCES)
    assert any("None" in v for v in result)


# --- rule 2: the quote must appear in the file it names --------------------

def test_a_quote_present_in_its_named_file_passes():
    assert validate_response(response(assertion()), SOURCES) == []


def test_whitespace_differences_do_not_fail_a_real_quote():
    # The model may re-wrap a line; that is formatting, not fabrication.
    quoted = "Nabil declared\n   a 12.50%   cash dividend"
    assert validate_response(response(assertion(quote=quoted)), SOURCES) == []


def test_a_quote_absent_from_the_file_is_flagged():
    result = validate_response(
        response(assertion(quote="Nabil declared a 30% dividend",
                           source_figure=None)),
        SOURCES,
    )
    assert len(result) == 1 and "does not appear" in result[0]


def test_a_quote_attributed_to_an_unsupplied_file_is_flagged():
    result = validate_response(
        response(assertion(source_file="invented.md")), SOURCES
    )
    assert any("not one of the files supplied" in v for v in result)


# --- rule 3: every number in the figure must appear in its own quote -------

def test_a_figure_whose_numbers_are_all_quoted_passes():
    assert validate_response(response(assertion()), SOURCES) == []


def test_a_descriptive_gloss_around_the_number_is_tolerated():
    # Rule 3 checks numbers, not the whole string: the gloss is the model's
    # own wording and makes no claim about the source.
    figure = "12.50% (cash dividend, FY 2081/2082)"
    quoted = "For FY 2081/2082 Nabil declared a 12.50% cash dividend."
    assert validate_response(
        response(assertion(source_figure=figure, quote=quoted)), SOURCES
    ) == []


def test_a_figure_not_present_in_its_quote_is_flagged():
    result = validate_response(
        response(assertion(source_figure="30%")), SOURCES
    )
    assert any("do not appear in the quote" in v for v in result)


def test_a_figure_offered_with_no_quote_is_flagged():
    result = validate_response(
        response(assertion(quote=None)), SOURCES
    )
    assert any("no quote" in v for v in result)


# --- shape -----------------------------------------------------------------

def test_a_non_object_response_is_rejected_outright():
    assert validate_response(["not", "an", "object"], SOURCES) == [
        "response is not a JSON object"
    ]


def test_a_response_with_no_assertions_is_clean():
    assert validate_response({"assertions": []}, SOURCES) == []


# --- known gaps ------------------------------------------------------------
# These pin behaviour the validator does NOT catch. They pass today. If a
# rule is tightened they will fail, which is the point: the failure is the
# reminder to update README.md and the report.

def test_known_gap_an_assertion_with_no_quote_is_never_flagged():
    """Rule 2 only inspects quotes that exist, so a bare verdict with no
    quote and no figure passes. The validator proves citations are
    well formed; it does not require that any be offered."""
    bare = response({"status": "verified"}, {"status": "contradicted"})
    assert validate_response(bare, SOURCES) == []


def test_known_gap_a_number_matches_inside_a_larger_number():
    """Rule 3 uses substring matching, so the figure 2.31 is satisfied by a
    quote containing 12.31. A wrong figure can pass if its digits happen to
    sit inside a right one."""
    sources = {"nabil.md": "the yield on money invested is 12.31%"}
    result = validate_response(
        response(assertion(source_figure="2.31%",
                           quote="the yield on money invested is 12.31%")),
        sources,
    )
    assert result == []


def test_known_gap_thousands_separators_must_match_exactly():
    """A figure written 4,839,903,472 is not found in a quote that writes
    the same number as 4839903472. This produces a false violation --
    the citation is correct and the validator says otherwise."""
    sources = {"ebl.md": "net profit of 4839903472 rupees"}
    result = validate_response(
        response(assertion(source_figure="4,839,903,472",
                           quote="net profit of 4839903472 rupees",
                           source_file="ebl.md")),
        sources,
    )
    assert len(result) == 1 and "do not appear" in result[0]


def test_known_gap_the_number_pattern_swallows_a_trailing_comma():
    """[\\d,]* is greedy, so a figure listing several numbers yields tokens
    carrying their separators -- '5,' rather than '5'. Those tokens rarely
    appear in a quote, so listing figures can produce false violations."""
    assert NUMBER.findall("5, 2, 4") == ["5,", "2,", "4"]


# --- runner ----------------------------------------------------------------

def main() -> int:
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failures = []

    for name, fn in tests:
        try:
            fn()
            print(f"  pass  {name}")
        except AssertionError as exc:
            failures.append((name, exc))
            print(f"  FAIL  {name}  {exc}")
        except Exception as exc:  # a raised error is also a failure
            failures.append((name, exc))
            print(f"  ERROR {name}  {type(exc).__name__}: {exc}")

    print(f"\n{len(tests) - len(failures)}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())