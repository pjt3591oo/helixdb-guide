# helix db 

```sh
$ uv sync
```

```sh
$ helix install
```

```sh
# generate config.hx.json, queries.hx, schema.hx on helixdb-cfg
$ helix init --path [PATH]
```

---

### sample run

default port: 6969

* run db

```sh
$ helix deploy --path helixdb-cfg

$ helix redeploy --path helixdb-cfg
```

* instance check

```sh
$ helix instances

Instance ID: b98151bf-4a56-4328-a235-b6962d568c6a (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /create_post
    └── /get_posts
    └── /get_followed_users_posts
    └── /get_posts_by_user
    └── /create_user
    └── /create_follow
    └── /get_followed_users
    └── /get_users
```

* run client

```sh
$ uv run main.py
```

* delete db

```sh
$ helix delete b98151bf-4a56-4328-a235-b6962d568c6a
```

### sample RAG

default port: 6969

* run db

```sh
$ helix deploy --path rag

$ helix redeploy --path rag
```

* instance check

```sh
$ helix instances

Instance ID: bef9e7a7-2ad2-476e-92a8-7a48a969f27a (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /loaddocs_rag
    └── /searchdocs_rag
```

* redeploy

```sh
$ helix redeploy --path rag  bef9e7a7-2ad2-476e-92a8-7a48a969f27a                                           ─╯

Helix instance found!
Successfully compiled 2 query files
Successfully wrote queries file
Successfully built Helix
Successfully started Helix instance
Instance ID: bef9e7a7-2ad2-476e-92a8-7a48a969f27a (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /loaddocs_rag
    └── /searchdocs_rag
```

* run client

```sh
$ uv run rag_demo_ml_papers.py
```

* delete db

```sh
$ helix delete bef9e7a7-2ad2-476e-92a8-7a48a969f27a
```
