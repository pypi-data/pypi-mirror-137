# This will become common across all SDKs so we can't assume it's going to flake cleanly.
# flake8: noqa

# Very generic find query
GQL_FRAGMENT_VARIABLES = """
fragment ppe_fields on Ppe {
  solveKey
  suggested
  max
  mean
  lastUpdatedTimestamp
}
fragment solverdata_fields on SolverData {
  solveKey
  BayesNetOutVertIDs
  BayesNetVertID
  dimIDs
  dimbw
  dims
  dimval
  dontmargin
  eliminated
  infoPerCoord
  initialized
  ismargin
  separator
  solveInProgress
  solvedCount
  variableType
  vecbw
  vecval
  _version
}
fragment variable_skeleton_fields on Variable {
	label
  tags
}
fragment variable_summary_fields on Variable {
  timestamp
  ppes {
    ...ppe_fields
  }
  variableType
  _version
}
fragment variable_full_fields on Variable{
  smallData
  solvable
  solverData
  {
		...solverdata_fields
  }
}
"""

GQL_FRAGMENT_FACTORS = """
fragment factor_skeleton_fields on Factor {
	label
  tags
  _variableOrderSymbols
}
fragment factor_summary_fields on Factor {
  timestamp
  _version
}
fragment factor_full_fields on Factor {
  fnctype
  solvable
  data
}
"""

GQL_GETVARIABLES = """
query sdk_get_variables(
  	$userId: ID!,
  	$robotIds: [ID!]!,
  	$sessionIds: [ID!]!,
    $variable_label_regexp: String = ".*",
    $variable_tags: [String] = ["VARIABLE"],
    $solvable: Int! = 0,
  	$fields_summary: Boolean! = false,
  	$fields_full: Boolean! = false){
	users(where: {id:$userId}) {
    name
		robots(where:{id_IN: $robotIds}) {
      name
      sessions(where:{id_IN: $sessionIds}){
        name
        variables(where:{
            label_MATCHES: $variable_label_regexp,
          	tags: $variable_tags,
          	solvable_GTE: $solvable}) {
          ...variable_skeleton_fields # Always include
          ...variable_summary_fields @include(if: $fields_summary)
          ...variable_full_fields @include(if: $fields_full)
        }
      }
    }
  }
}"""

GQL_GETFACTORS = """
query sdk_get_factors(
  	$userId: ID!,
  	$robotIds: [ID!]!,
  	$sessionIds: [ID!]!,
    $factor_label_regexp: String = ".*",
    $factor_tags: [String] = ["FACTOR"],
    $solvable: Int! = 0,
  	$fields_summary: Boolean! = false,
  	$fields_full: Boolean! = false){
	users(where: {id:$userId}) {
    name
		robots(where:{id_IN: $robotIds}) {
      name
      sessions(where:{id_IN: $sessionIds}){
        name
        factors(where:{
            label_MATCHES: $factor_label_regexp,
          	tags: $factor_tags,
          	solvable_GTE: $solvable}) {
          ...factor_skeleton_fields # Always include
          ...factor_summary_fields @include(if: $fields_summary)
          ...factor_full_fields @include(if: $fields_full)
        }
      }
    }
  }
}"""


GQL_GETVARIABLESFACTORS = """
query sdk_get_variablesfactors(
  	$userId: ID!,
  	$robotIds: [ID!]!,
  	$sessionIds: [ID!]!,
  	$variables: Boolean! = true,
  	$factors: Boolean! = true,
    $variable_label_regexp: String = ".*",
    $factor_label_regexp: String = ".*",
    $variable_tags: [String] = ["VARIABLE"],
    $factor_tags: [String] = ["FACTOR"],
    $solvable: Int! = 0,
  	$fields_summary: Boolean! = false,
  	$fields_full: Boolean! = false){
	users(where:{id: $userId}) {
    name
		robots(where:{id_IN: $robotIds}) {
      name
      sessions(where:{id_IN: $sessionIds}){
        name
        variables(where:{
            label_MATCHES: $variable_label_regexp,
          	tags: $variable_tags,
          	solvable_GTE: 0}) @include(if: $variables){
          ...variable_skeleton_fields # Always include
          ...variable_summary_fields @include(if: $fields_summary)
          ...variable_full_fields @include(if: $fields_full)
        }
        factors(filter:{
            label_MATCHES: $factor_label_regexp,
          	tags: $factor_tags,
          	solvable_GTE: $solvable}) @include(if: $factors){
          ...factor_skeleton_fields # Always include
          ...factor_summary_fields @include(if: $fields_summary)
          ...factor_full_fields @include(if: $fields_full)
        }
      }
    }
  }
}"""


GQL_GETVARIABLE = """
query sdk_get_variable(
  	$userId: ID!,
  	$robotId: ID!,
  	$sessionId: ID!,
    $label: ID!) {
	users(where:{id: $userId}) {
		robots(where:{id: $robotId}) {
      sessions(where:{id: $sessionId}) {
        variables(where:{label: $label}) {
          ...variable_skeleton_fields
          ...variable_summary_fields
          ...variable_full_fields
        }
      }
    }
  }
}"""


GQL_GETFACTOR = """
query sdk_get_variable(
  	$userId: ID!,
  	$robotId: ID!,
  	$sessionId: ID!,
    $label: ID!) {
	users(where:{id: $userId}) {
		robots(where:{id: $robotId}) {
      sessions(where:{id: $sessionId}) {
        factors(where:{label: $label}) {
          ...factor_skeleton_fields
          ...factor_summary_fields
          ...factor_full_fields
        }
      }
    }
  }
}"""


GQL_GETSTATUSMESSAGES = """
query sdk_ls_statusmessages($id: ID!) {
    statusMessages(id: $id) {
        requestId,
        action,
        state,
        timestamp,
        client {
            userId,
            robotId,
            sessionId
        }
    }
}
"""

GQL_GETSTATUSLATEST = """
query sdk_get_statuslatest($id: ID!) {
  statusLatest(id: $id) {
    requestId,
    action,
    state,
    timestamp,
    client {
      userId,
      robotId,
      sessionId
    }
  }
}
"""
