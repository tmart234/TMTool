# this form helps modelers describe the data flows within their model
# this script takes all model "flows" (stencil obj as dictionary) & then sets CIA + severity metrics for each flow
# Note: a model should also contain flows describing how data-at-rest gets stored/extracted from a system
#   since threats are generated based on flows, CIA is also infered from flows
# TODO: also have notes and justification as text input
# TODO: since severity is a threat prop, for (some) threats we could store it in the template and chose worst case
#        PyTM uses severity as a threat property: https://github.com/izar/pytm/blob/master/docs/threats.md


def main(flows):
    print(flows)

if __name__ == '__main__':
   main()