function init() {
  var $ = go.GraphObject.make  // for conciseness in defining templates

  myDiagram = $(go.Diagram, "myDiagramDiv",  // must name or refer to the DIV HTML element
    {
      initialContentAlignment: go.Spot.Left,
      allowSelect: false,  // the user cannot select any part
      // create a TreeLayout for the decision tree
      layout: $(go.TreeLayout)
    })

  // get the text for the tooltip from the data on the object being hovered over
  function tooltipTextConverter(data) {
    var str = ""
    var e = myDiagram.lastInput
    var currobj = e.targetObject
    if (currobj !== null && (currobj.name === "ButtonA" ||
      (currobj.panel !== null && currobj.panel.name === "ButtonA"))) {
      str = data.aToolTip
    } else {
      str = data.bToolTip
    }
    return str
  }

  // define tooltips for buttons
  var tooltipTemplate =
    $("ToolTip",
      { "Border.fill": "whitesmoke", "Border.stroke": "lightgray" },
      $(go.TextBlock,
        {
          font: "8pt sans-serif",
          wrap: go.TextBlock.WrapFit,
          desiredSize: new go.Size(200, NaN),
          alignment: go.Spot.Center,
          margin: 6
        },
        new go.Binding("text", "", tooltipTextConverter))
    )

  // define the Node template for non-leaf nodes
  myDiagram.nodeTemplateMap.add("decision",
    $(go.Node, "Auto",
      new go.Binding("text", "key"),
      // define the node's outer shape, which will surround the Horizontal Panel
      $(go.Shape, "Rectangle",
        { fill: "whitesmoke", stroke: "lightgray" }),
      // define a horizontal Panel to place the node's text alongside the buttons
      $(go.Panel, "Horizontal",
        $(go.TextBlock,
          { font: "20px Roboto, sans-serif", margin: 5 },
          new go.Binding("text", "key")),
        // define a vertical panel to place the node's two buttons one above the other
        $(go.Panel, "Vertical",
          { defaultStretch: go.GraphObject.Fill, margin: 3 },
          $("Button",  // button A
            {
              name: "ButtonA",
              toolTip: tooltipTemplate
            },
            new go.Binding("portId", "a"),
            $(go.TextBlock,
              { font: '500 12px Roboto, sans-serif' },
              new go.Binding("text", "aText"))
          ),  // end button A
          $("Button",  // button B
            {
              name: "ButtonB",
              toolTip: tooltipTemplate
            },
            new go.Binding("portId", "b"),
            $(go.TextBlock,
              { font: '500 12px Roboto, sans-serif' },
              new go.Binding("text", "bText"))
          )  // end button B
        )  // end Vertical Panel
      )  // end Horizontal Panel
    ))  // end Node and call to add

  // define the Node template for leaf nodes
  myDiagram.nodeTemplateMap.add("personality",
    $(go.Node, "Auto",
      new go.Binding("text", "key"),
      $(go.Shape, "Rectangle",
        { fill: "whitesmoke", stroke: "lightgray" }),
      $(go.TextBlock,
        {
          font: '13px Roboto, sans-serif',
          wrap: go.TextBlock.WrapFit, desiredSize: new go.Size(200, NaN), margin: 5
        },
        new go.Binding("text", "text"))
    ))

  // define the only Link template
  myDiagram.linkTemplate =
    $(go.Link, go.Link.Orthogonal,  // the whole link panel
      { fromPortId: "" },
      new go.Binding("fromPortId", "fromport"),
      $(go.Shape,  // the link shape
        { stroke: "lightblue", strokeWidth: 2 })
    )

  // create the model for the decision tree
  var model =
    $(go.GraphLinksModel,
      { linkFromPortIdProperty: "fromport" })
  // set up the model with the node and link data
  makeMyNodes(model)
  makeMyLinks(model)
  console.log(model.nodeDataArray)
  console.log(model.linkDataArray)
  myDiagram.model = model
}

function readJsonFromFile(file) {
	let json
	$.ajaxSettings.async = false
	$.get(file).done(function(data) {
		json = data
	})
	return json
}

function makeMyNodes(model) {
	let tree = readJsonFromFile('../tree.json')
  var nodeDataArray = []
  
  let tmp = new Object()
  tmp.key = 'Start'
  tmp.category = 'decision'
  tmp.a = addNodeFromTree(nodeDataArray, tree.left).key
  tmp.aText = '<= ' + tree.key
  tmp.b = addNodeFromTree(nodeDataArray, tree.right).key
  tmp.bText = '> ' + tree.key
  nodeDataArray.push(tmp)

  model.nodeDataArray = nodeDataArray
}

function addNodeFromTree(nodeDataArray, node) {
  if (node === null) return null
  let tmp = new Object()
  if (node.result === null) {
    node.key = node.key.toFixed(2)
		tmp.key = node.attribute + ':' + node.key
    tmp.category = 'decision'
    tmp.a = addNodeFromTree(nodeDataArray, node.left).key
    tmp.aText = '<= ' + node.key
    tmp.b = addNodeFromTree(nodeDataArray, node.right).key
    tmp.bText = '> ' + node.key
  } else {
    tmp.key = node.result + Math.random().toFixed(4)
    tmp.category = 'personality'
    tmp.text = node.result
  }
  nodeDataArray.push(tmp)
  return tmp
}

function makeMyLinks(model) {
  var linkDataArray = []
  var nda = model.nodeDataArray
  for (var i = 0; i < nda.length; i++) {
    if (nda[i].key === 'Start') {
      linkDataArray.push({ from: nda[i].key, fromport: nda[i].a, to: nda[i].a })
      linkDataArray.push({ from: nda[i].key, fromport: nda[i].b, to: nda[i].b })
      continue
    }
    if (nda[i].a != undefined) {
      linkDataArray.push({ from: nda[i].key, fromport: nda[i].a, to: nda[i].a })
    }
    if (nda[i].b != undefined) {
      linkDataArray.push({ from: nda[i].key, fromport: nda[i].b, to: nda[i].b })
    }
  }
  model.linkDataArray = linkDataArray
}