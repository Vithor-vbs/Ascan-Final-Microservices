import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  let comment = "";
  const [description, setDescription] = useState("");
  const [isVariableTrue, setIsVariableTrue] = useState(false);

  

  useEffect(() => {
    (async () => {
      const response = await fetch("http://localhost:8000/api/posts");

      const content = await response.json();

      setPosts(content);
    })();
  }, []);

  const createPost = async (e) => {
    e.preventDefault();

    const existingPost = posts.find((post) => post.title === title);
    if (existingPost) {
      // Email already exists, update the description of the existing post
      if (isVariableTrue) {
        await deletePost(existingPost.id);
        return;
      }

      const updatedPost = { ...existingPost, description };
      const res = await fetch(
        `http://localhost:8000/api/posts/${existingPost.id}`,
        {
          method: "PUT", 
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(updatedPost),
        }
      );

      const updatedData = await res.json();
      console.log("Post updated:", updatedData);

      // Update the posts state with the modified post
      setPosts(
        posts.map((post) => (post.id === updatedData.id ? updatedData : post))
      );
    } else {
      // Email does not exist, create a new post
      const res = await fetch("http://localhost:8000/api/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          description,
        }),
      });

      const createdPost = await res.json();

      setPosts([...posts, createdPost]);
    }
  };

  const deletePost = async (postId) => {
    try {
      await fetch(`http://localhost:8000/api/posts/${postId}`, {
        method: "DELETE",
      });

      setIsVariableTrue(false);

      setPosts(posts.filter((post) => post.id !== postId));
    } catch (error) {
      console.log("Error deleting post:", error);
    }
  };

  const createComment = async (e, post_id) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8001/api/comments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        post_id,
        text: comment,
      }),
    });

    const createdComment = await response.json();

    comment = "";

    setPosts(
      posts.map((p) => {
        if (p.id === post_id) {
          if (!p.comments) {
            p.comments = [];
          }
          p.comments.push(createdComment);
        }

        return p;
      })
    );
  };

  const handleAssignButtonClick = () => {
    setDescription("Subscription Purchased");
  };
  const handleCancelSubscription = () => {
    setDescription("Subscription Cancelled");
  };
  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };
  const handleClick = () => {
    setIsVariableTrue(true);
  };
  return (
    <div className="App container">
      <form className="row headers-box" onSubmit={createPost}>
        <div className="col-4">
          <h2 className="header">Cart Administrator</h2>

          <input
            className="form-control mb-3 dark-color"
            placeholder="Enter your email"
            onChange={handleTitleChange}
          />
          <div className="button-box">
            <button
              className="btn btn-primary assign-button"
              type="submit"
              onClick={handleAssignButtonClick}
            >
              Assign
            </button>
            {posts.some((post) => post.title === title) && (
              <button
                className="btn btn-secundary"
                onClick={handleCancelSubscription}
              >
                Cancel
              </button>
            )}
            {posts.some((post) => post.title === title) && (
              <button
                className="btn btn-delete"
                onClick={handleClick}
              >
                Remove User
              </button>
            )}
          </div>
        </div>
      </form>

      <main>
        <div className="row row-cols-1 row-cols-md-3 mb-3 text-center">
          {posts.length &&
            posts.map((post) => {
              return (
                <div className="col" key={post.id}>
                  <div className="card mb-4 rounded-3 shadow-sm darkest-color">
                    <div className="card-header py-3">
                      <h4 className="my-0 fw-normal">{post.title}</h4>
                    </div>
                    <div className="card-body">
                      <p
                        className={`card-title pricing-card-title ${
                          post.description === "Subscription Cancelled"
                            ? "cancelled-description"
                            : ""
                        } ${
                          post.description === "Subscription Purchased"
                            ? "purchased-description"
                            : ""
                        }`}
                      >
                        {post.description}
                      </p>
                      <form onSubmit={(e) => createComment(e, post.id)}>
                        <input
                          className="w-100 form-control dark-color"
                          onChange={(e) => (comment = e.target.value)}
                        />
                      </form>
                    </div>
                    {post.comments &&
                      post.comments.map((comment) => {
                        return (
                          <div className="card-footer py-3" key={comment.id}>
                            {comment.text}
                          </div>
                        );
                      })}
                  </div>
                </div>
              );
            })}
        </div>
      </main>
    </div>
  );
}

export default App;
