
QUERY CreateUser(name: String, age: U32, email: String, now: I32) => 
    user <- AddN<User>({name: name, age: age, email: email, created_at: now, updated_at: now}) 
    RETURN user

QUERY CreateFollow(follower_uid: U128, followed_uid: U128, now: I32) => 
    follower <- N<User>(follower_uid) 
    followed <- N<User>(followed_uid) 
    AddE<Follows>({since: now})::From(follower)::To(followed)
    RETURN "success"

QUERY CreatePost(author_uid: U128, content: String, now: I32) => 
    user <- N<User>(author_uid) 
    post <- AddN<Post>({content: content, created_at: now, updated_at: now}) 
    AddE<Created>({created_at: now})::From(user)::To(post)
    RETURN post

QUERY GetUsers() =>
    users <- N<User>
    RETURN users

QUERY GetPosts() =>
    posts <- N<Post>
    RETURN posts


QUERY GetPostsByUser(author_uid: U128) =>
    posts <- N<User>(author_uid)::Out<Created>
    RETURN posts

QUERY GetFollowedUsers(user_uid: U128) =>
    followed <- N<User>(user_uid)::Out<Follows>
    RETURN followed

QUERY GetFollowedUsersPosts(user_uid: U128) =>
    followers <- N<User>(user_uid)::Out<Follows>
    posts <- followers::Out<Created>::RANGE(0, 40)
    RETURN posts::{
        content: content, 
        creatorID: _::In<Created>::ID, 
    }