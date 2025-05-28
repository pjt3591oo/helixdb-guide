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

* deploy

```sh
$ helix deploy --path helixdb-cfg

Successfully compiled 2 query files
Successfully transpiled queries
Successfully wrote queries file
Successfully built Helix
Successfully started Helix instance
Instance ID: 6c7af21f-1fbc-47d6-ad71-43ba9816bf83 (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /create_follow
    └── /create_user
    └── /get_posts
    └── /get_users
    └── /get_followed_users_posts
    └── /get_followed_users
    └── /create_post
    └── /get_posts_by_user
```

* redeploy

```sh
$ helix redeploy --path helixdb-cfg 6c7af21f-1fbc-47d6-ad71-43ba9816bf83

Helix instance found!
Successfully compiled 2 query files
Successfully wrote queries file
Successfully built Helix
Successfully started Helix instance
Instance ID: 6c7af21f-1fbc-47d6-ad71-43ba9816bf83 (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /get_posts_by_user
    └── /get_followed_users_posts
    └── /create_follow
    └── /get_followed_users
    └── /get_users
    └── /create_user
    └── /create_post
    └── /get_posts
```

* instance check

```sh
$ helix instances

Instance ID: 6c7af21f-1fbc-47d6-ad71-43ba9816bf83 (running)
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
$ helix delete 6c7af21f-1fbc-47d6-ad71-43ba9816bf83
```

### sample RAG

default port: 6969

* run db

```sh
$ helix deploy --path rag

Successfully compiled 2 query files
Successfully transpiled queries
Successfully wrote queries file
Successfully built Helix
Successfully started Helix instance
Instance ID: 470f7297-04c3-4185-80ed-15cb859175f7 (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /loaddocs_rag
    └── /searchdocs_rag
```

* redeploy

```sh
$ helix redeploy --path rag  470f7297-04c3-4185-80ed-15cb859175f7

Helix instance found!
Successfully compiled 2 query files
Successfully wrote queries file
Successfully built Helix
Successfully started Helix instance
Instance ID: 470f7297-04c3-4185-80ed-15cb859175f7 (running)
└── Label: 
└── Port: 6969
└── Available endpoints:
    └── /searchdocs_rag
    └── /loaddocs_rag
```

* instance check

```sh
$ helix instances

Instance ID: 470f7297-04c3-4185-80ed-15cb859175f7 (running)
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
$ helix delete 470f7297-04c3-4185-80ed-15cb859175f7
```
