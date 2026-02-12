from enum import Enum

class Alignment(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"
    CENTER = "CENTER"

class AnnulusWedgeCriteria(str, Enum):
    LEAF_NUMBER = "LEAF_NUMBER"
    NODE_SIZE = "NODE_SIZE"

class BoxLayoutProvider_PackingMode(str, Enum):
    SIMPLE = "SIMPLE"
    GROUP_DEC = "GROUP_DEC"
    GROUP_MIXED = "GROUP_MIXED"
    GROUP_INC = "GROUP_INC"

class CenterEdgeLabelPlacementStrategy(str, Enum):
    MEDIAN_LAYER = "MEDIAN_LAYER"
    TAIL_LAYER = "TAIL_LAYER"
    HEAD_LAYER = "HEAD_LAYER"
    SPACE_EFFICIENT_LAYER = "SPACE_EFFICIENT_LAYER"

class ComponentOrderingStrategy(str, Enum):
    NONE = "NONE"
    INSIDE_PORT_SIDE_GROUPS = "INSIDE_PORT_SIDE_GROUPS"
    GROUP_MODEL_ORDER = "GROUP_MODEL_ORDER"
    MODEL_ORDER = "MODEL_ORDER"

class ConstraintCalculationStrategy(str, Enum):
    QUADRATIC = "QUADRATIC"
    SCANLINE = "SCANLINE"

class ContentAlignment(str, Enum):
    V_TOP = "V_TOP"
    V_CENTER = "V_CENTER"
    V_BOTTOM = "V_BOTTOM"
    H_LEFT = "H_LEFT"
    H_CENTER = "H_CENTER"
    H_RIGHT = "H_RIGHT"

class CrossingMinimizationStrategy(str, Enum):
    LAYER_SWEEP = "LAYER_SWEEP"
    MEDIAN_LAYER_SWEEP = "MEDIAN_LAYER_SWEEP"
    NONE = "NONE"

class CuttingStrategy(str, Enum):
    ARD = "ARD"
    MSD = "MSD"
    MANUAL = "MANUAL"

class CycleBreakingStrategy(str, Enum):
    GREEDY = "GREEDY"
    DEPTH_FIRST = "DEPTH_FIRST"
    MODEL_ORDER = "MODEL_ORDER"
    GREEDY_MODEL_ORDER = "GREEDY_MODEL_ORDER"
    SCC_CONNECTIVITY = "SCC_CONNECTIVITY"
    SCC_NODE_TYPE = "SCC_NODE_TYPE"
    DFS_NODE_ORDER = "DFS_NODE_ORDER"
    BFS_NODE_ORDER = "BFS_NODE_ORDER"

class Direction(str, Enum):
    UNDEFINED = "UNDEFINED"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    DOWN = "DOWN"
    UP = "UP"

class DirectionCongruency(str, Enum):
    READING_DIRECTION = "READING_DIRECTION"
    ROTATION = "ROTATION"

class DiscoCompactionStrategy(str, Enum):
    POLYOMINO = "POLYOMINO"

class EdgeCoords(str, Enum):
    INHERIT = "INHERIT"
    CONTAINER = "CONTAINER"
    PARENT = "PARENT"
    ROOT = "ROOT"

class EdgeLabelPlacement(str, Enum):
    CENTER = "CENTER"
    HEAD = "HEAD"
    TAIL = "TAIL"

class EdgeLabelSideSelection(str, Enum):
    ALWAYS_UP = "ALWAYS_UP"
    ALWAYS_DOWN = "ALWAYS_DOWN"
    DIRECTION_UP = "DIRECTION_UP"
    DIRECTION_DOWN = "DIRECTION_DOWN"
    SMART_UP = "SMART_UP"
    SMART_DOWN = "SMART_DOWN"

class EdgeRouting(str, Enum):
    UNDEFINED = "UNDEFINED"
    POLYLINE = "POLYLINE"
    ORTHOGONAL = "ORTHOGONAL"
    SPLINES = "SPLINES"

class EdgeRoutingMode(str, Enum):
    NONE = "NONE"
    MIDDLE_TO_MIDDLE = "MIDDLE_TO_MIDDLE"
    AVOID_OVERLAP = "AVOID_OVERLAP"

class EdgeRoutingStrategy(str, Enum):
    STRAIGHT = "STRAIGHT"
    BEND = "BEND"

class EdgeStraighteningStrategy(str, Enum):
    NONE = "NONE"
    IMPROVE_STRAIGHTNESS = "IMPROVE_STRAIGHTNESS"

class EdgeType(str, Enum):
    NONE = "NONE"
    DIRECTED = "DIRECTED"
    UNDIRECTED = "UNDIRECTED"
    ASSOCIATION = "ASSOCIATION"
    GENERALIZATION = "GENERALIZATION"
    DEPENDENCY = "DEPENDENCY"

class FixedAlignment(str, Enum):
    NONE = "NONE"
    LEFTUP = "LEFTUP"
    RIGHTUP = "RIGHTUP"
    LEFTDOWN = "LEFTDOWN"
    RIGHTDOWN = "RIGHTDOWN"
    BALANCED = "BALANCED"

class ForceModelStrategy(str, Enum):
    EADES = "EADES"
    FRUCHTERMAN_REINGOLD = "FRUCHTERMAN_REINGOLD"

class GraphCompactionStrategy(str, Enum):
    NONE = "NONE"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    LEFT_RIGHT_CONSTRAINT_LOCKING = "LEFT_RIGHT_CONSTRAINT_LOCKING"
    LEFT_RIGHT_CONNECTION_LOCKING = "LEFT_RIGHT_CONNECTION_LOCKING"
    EDGE_LENGTH = "EDGE_LENGTH"

class GreedySwitchType(str, Enum):
    ONE_SIDED = "ONE_SIDED"
    TWO_SIDED = "TWO_SIDED"
    OFF = "OFF"

class GroupOrderStrategy(str, Enum):
    ONLY_WITHIN_GROUP = "ONLY_WITHIN_GROUP"
    MODEL_ORDER = "MODEL_ORDER"
    ENFORCED = "ENFORCED"

class HierarchyHandling(str, Enum):
    INHERIT = "INHERIT"
    INCLUDE_CHILDREN = "INCLUDE_CHILDREN"
    SEPARATE_CHILDREN = "SEPARATE_CHILDREN"

class HighLevelSortingCriterion(str, Enum):
    NUM_OF_EXTERNAL_SIDES_THAN_NUM_OF_EXTENSIONS_LAST = "NUM_OF_EXTERNAL_SIDES_THAN_NUM_OF_EXTENSIONS_LAST"
    CORNER_CASES_THAN_SINGLE_SIDE_LAST = "CORNER_CASES_THAN_SINGLE_SIDE_LAST"

class InteractiveReferencePoint(str, Enum):
    CENTER = "CENTER"
    TOP_LEFT = "TOP_LEFT"

class LayerConstraint(str, Enum):
    NONE = "NONE"
    FIRST = "FIRST"
    FIRST_SEPARATE = "FIRST_SEPARATE"
    LAST = "LAST"
    LAST_SEPARATE = "LAST_SEPARATE"

class LayerUnzippingStrategy(str, Enum):
    NONE = "NONE"
    ALTERNATING = "ALTERNATING"

class LayeringStrategy(str, Enum):
    NETWORK_SIMPLEX = "NETWORK_SIMPLEX"
    LONGEST_PATH = "LONGEST_PATH"
    LONGEST_PATH_SOURCE = "LONGEST_PATH_SOURCE"

class LongEdgeOrderingStrategy(str, Enum):
    DUMMY_NODE_OVER = "DUMMY_NODE_OVER"
    DUMMY_NODE_UNDER = "DUMMY_NODE_UNDER"
    EQUAL = "EQUAL"

class LowLevelSortingCriterion(str, Enum):
    BY_SIZE = "BY_SIZE"
    BY_SIZE_AND_SHAPE = "BY_SIZE_AND_SHAPE"

class NeatoModel(str, Enum):
    SHORTPATH = "SHORTPATH"
    CIRCUIT = "CIRCUIT"
    SUBSET = "SUBSET"

class NodeArrangementStrategy(str, Enum):
    LEFT_RIGHT_TOP_DOWN_NODE_PLACER = "LEFT_RIGHT_TOP_DOWN_NODE_PLACER"

class NodeFlexibility(str, Enum):
    NONE = "NONE"
    PORT_POSITION = "PORT_POSITION"
    NODE_SIZE = "NODE_SIZE"

class NodeLabelPlacement(str, Enum):
    H_LEFT = "H_LEFT"
    H_CENTER = "H_CENTER"
    H_RIGHT = "H_RIGHT"
    V_TOP = "V_TOP"
    V_CENTER = "V_CENTER"
    V_BOTTOM = "V_BOTTOM"
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    H_PRIORITY = "H_PRIORITY"

class NodePlacementStrategy(str, Enum):
    SIMPLE = "SIMPLE"
    LINEAR_SEGMENTS = "LINEAR_SEGMENTS"
    BRANDES_KOEPF = "BRANDES_KOEPF"
    NETWORK_SIMPLEX = "NETWORK_SIMPLEX"

class NodePromotionStrategy(str, Enum):
    NONE = "NONE"
    NIKOLOV = "NIKOLOV"
    NIKOLOV_PIXEL = "NIKOLOV_PIXEL"
    MODEL_ORDER_LEFT_TO_RIGHT = "MODEL_ORDER_LEFT_TO_RIGHT"
    MODEL_ORDER_RIGHT_TO_LEFT = "MODEL_ORDER_RIGHT_TO_LEFT"

class OptimizationGoal(str, Enum):
    ASPECT_RATIO_DRIVEN = "ASPECT_RATIO_DRIVEN"
    MAX_SCALE_DRIVEN = "MAX_SCALE_DRIVEN"
    AREA_DRIVEN = "AREA_DRIVEN"

class OrderWeighting(str, Enum):
    MODEL_ORDER = "MODEL_ORDER"
    DESCENDANTS = "DESCENDANTS"
    FAN = "FAN"
    CONSTRAINT = "CONSTRAINT"

class OrderingStrategy(str, Enum):
    NONE = "NONE"
    NODES_AND_EDGES = "NODES_AND_EDGES"
    PREFER_EDGES = "PREFER_EDGES"
    PREFER_NODES = "PREFER_NODES"

class OverlapMode(str, Enum):
    NONE = "NONE"
    SCALE = "SCALE"
    SCALEXY = "SCALEXY"
    PRISM = "PRISM"
    COMPRESS = "COMPRESS"

class PackingStrategy(str, Enum):
    COMPACTION = "COMPACTION"
    SIMPLE = "SIMPLE"
    NONE = "NONE"

class PortAlignment(str, Enum):
    DISTRIBUTED = "DISTRIBUTED"
    JUSTIFIED = "JUSTIFIED"
    BEGIN = "BEGIN"
    CENTER = "CENTER"
    END = "END"

class PortConstraints(str, Enum):
    UNDEFINED = "UNDEFINED"
    FREE = "FREE"
    FIXED_SIDE = "FIXED_SIDE"
    FIXED_ORDER = "FIXED_ORDER"
    FIXED_RATIO = "FIXED_RATIO"
    FIXED_POS = "FIXED_POS"

class PortLabelPlacement(str, Enum):
    OUTSIDE = "OUTSIDE"
    INSIDE = "INSIDE"
    NEXT_TO_PORT_IF_POSSIBLE = "NEXT_TO_PORT_IF_POSSIBLE"
    ALWAYS_SAME_SIDE = "ALWAYS_SAME_SIDE"
    ALWAYS_OTHER_SAME_SIDE = "ALWAYS_OTHER_SAME_SIDE"
    SPACE_EFFICIENT = "SPACE_EFFICIENT"

class PortSide(str, Enum):
    UNDEFINED = "UNDEFINED"
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

class PortSortingStrategy(str, Enum):
    INPUT_ORDER = "INPUT_ORDER"
    PORT_DEGREE = "PORT_DEGREE"

class RadialCompactionStrategy(str, Enum):
    NONE = "NONE"
    RADIAL_COMPACTION = "RADIAL_COMPACTION"
    WEDGE_COMPACTION = "WEDGE_COMPACTION"

class RadialTranslationStrategy(str, Enum):
    NONE = "NONE"
    EDGE_LENGTH = "EDGE_LENGTH"
    CROSSING_MINIMIZATION_BY_POSITION = "CROSSING_MINIMIZATION_BY_POSITION"

class RootSelection(str, Enum):
    FIXED = "FIXED"
    CENTER_NODE = "CENTER_NODE"

class SelfLoopDistributionStrategy(str, Enum):
    EQUALLY = "EQUALLY"
    NORTH = "NORTH"
    NORTH_SOUTH = "NORTH_SOUTH"

class SelfLoopOrderingStrategy(str, Enum):
    STACKED = "STACKED"
    REVERSE_STACKED = "REVERSE_STACKED"
    SEQUENCED = "SEQUENCED"

class ShapeCoords(str, Enum):
    INHERIT = "INHERIT"
    PARENT = "PARENT"
    ROOT = "ROOT"

class SizeConstraint(str, Enum):
    PORTS = "PORTS"
    PORT_LABELS = "PORT_LABELS"
    NODE_LABELS = "NODE_LABELS"
    MINIMUM_SIZE = "MINIMUM_SIZE"

class SizeOptions(str, Enum):
    DEFAULT_MINIMUM_SIZE = "DEFAULT_MINIMUM_SIZE"
    MINIMUM_SIZE_ACCOUNTS_FOR_PADDING = "MINIMUM_SIZE_ACCOUNTS_FOR_PADDING"
    COMPUTE_PADDING = "COMPUTE_PADDING"
    OUTSIDE_NODE_LABELS_OVERHANG = "OUTSIDE_NODE_LABELS_OVERHANG"
    PORTS_OVERHANG = "PORTS_OVERHANG"
    UNIFORM_PORT_SPACING = "UNIFORM_PORT_SPACING"
    FORCE_TABULAR_NODE_LABELS = "FORCE_TABULAR_NODE_LABELS"
    ASYMMETRICAL = "ASYMMETRICAL"

class SortingStrategy(str, Enum):
    NONE = "NONE"
    ID = "ID"

class SpanningTreeCostFunction(str, Enum):
    CENTER_DISTANCE = "CENTER_DISTANCE"
    CIRCLE_UNDERLAP = "CIRCLE_UNDERLAP"
    RECTANGLE_UNDERLAP = "RECTANGLE_UNDERLAP"
    INVERTED_OVERLAP = "INVERTED_OVERLAP"
    MINIMUM_ROOT_DISTANCE = "MINIMUM_ROOT_DISTANCE"

class SplineRoutingMode(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    CONSERVATIVE_SOFT = "CONSERVATIVE_SOFT"
    SLOPPY = "SLOPPY"

class SporeCompactionStrategy(str, Enum):
    DEPTH_FIRST = "DEPTH_FIRST"

class StressMajorization_Dimension(str, Enum):
    XY = "XY"
    X = "X"
    Y = "Y"

class StructureExtractionStrategy(str, Enum):
    DELAUNAY_TRIANGULATION = "DELAUNAY_TRIANGULATION"

class TopdownNodeTypes(str, Enum):
    PARALLEL_NODE = "PARALLEL_NODE"
    HIERARCHICAL_NODE = "HIERARCHICAL_NODE"
    ROOT_NODE = "ROOT_NODE"

class TraversalStrategy(str, Enum):
    SPIRAL = "SPIRAL"
    LINE_BY_LINE = "LINE_BY_LINE"
    MANHATTAN = "MANHATTAN"
    JITTER = "JITTER"
    QUADRANTS_LINE_BY_LINE = "QUADRANTS_LINE_BY_LINE"
    QUADRANTS_MANHATTAN = "QUADRANTS_MANHATTAN"
    QUADRANTS_JITTER = "QUADRANTS_JITTER"
    COMBINE_LINE_BY_LINE_MANHATTAN = "COMBINE_LINE_BY_LINE_MANHATTAN"
    COMBINE_JITTER_MANHATTAN = "COMBINE_JITTER_MANHATTAN"

class TreeConstructionStrategy(str, Enum):
    MINIMUM_SPANNING_TREE = "MINIMUM_SPANNING_TREE"
    MAXIMUM_SPANNING_TREE = "MAXIMUM_SPANNING_TREE"

class TreeifyingOrder(str, Enum):
    DFS = "DFS"
    BFS = "BFS"

class ValidifyStrategy(str, Enum):
    NO = "NO"
    GREEDY = "GREEDY"
    LOOK_BACK = "LOOK_BACK"

class WhiteSpaceEliminationStrategy(str, Enum):
    EQUAL_BETWEEN_STRUCTURES = "EQUAL_BETWEEN_STRUCTURES"
    TO_ASPECT_RATIO = "TO_ASPECT_RATIO"
    NONE = "NONE"

class WhitespaceEliminationStrategy(str, Enum):
    BOTTOM_ROW_EQUAL_WHITESPACE_ELIMINATOR = "BOTTOM_ROW_EQUAL_WHITESPACE_ELIMINATOR"

class WidthApproximationStrategy(str, Enum):
    GREEDY = "GREEDY"
    TARGET_WIDTH = "TARGET_WIDTH"

class WrappingStrategy(str, Enum):
    OFF = "OFF"
    SINGLE_EDGE = "SINGLE_EDGE"
    MULTI_EDGE = "MULTI_EDGE"

# Backward-compatible aliases
NodeSizeConstraint = SizeConstraint
NodeSizeOption = SizeOptions
PortConstraint = PortConstraints
