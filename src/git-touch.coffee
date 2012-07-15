fill =
    "stroke": "#fff"
    "fill": "#fff"
    "fill-opacity": .5
    "stroke-width": 2
    "stroke-linecap": "round"
    "stroke-linejoin": "round"

$(document).onresize = ->
    r = Raphael("holder").setSize(window.innerWidth, window.innerHeight)

$(document).ready ->
    r = Raphael("holder")
    conn_commits = [] # [commit.sha1, parent.sha1]
    connections = [] # lines
    shape_size = 10 # make is big so I can touch it
    # where to start drawing (center of the window)
    center_h = Math.ceil(window.innerHeight / 2)
    center_w = Math.ceil(window.innerWidth / 2)
    commits = {}
    $.getJSON GIT_TOUCH_BASE_URL + "commits", (commit) ->
        parseTree commit
        drawConnections()

    spacing = 0
    parseTree = (commit) ->
        color = Raphael.getColor()
        r_commit = r.circle(center_w, center_h + spacing, shape_size).attr(fill).attr(
            fill: color # changing the color to a random one
            stroke: color
        ).data("commit", commit)
        spacing += 30  # add spacing between commits
        commits[commit.commit] = r_commit
        for i of commit.parents
            commit_parent = commit.parents[i]
            conn_commits.push [ commit.commit, commit_parent.commit ]
            parseTree commit_parent

    drawConnections = ->
        for i of conn_commits
            r_commit = commits[conn_commits[i][0]]
            r_parent = commits[conn_commits[i][1]]
            r_conn = r.connection(r_commit, r_parent, "#fff")
            connections.push r_conn
    hover_in = (e) ->
        rect = r.rect(e.x + 20, e.y + 20, 100, 75, 10).attr(text: "Hdsadas")
        @data "tooltip", rect.id

    hover_out = (e) ->
        r.getById(@data("tooltip")).remove()

