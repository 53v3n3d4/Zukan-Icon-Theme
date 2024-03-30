// Author: https://github.com/mauroreisvieira/github-sublime-theme/
import { useState } from 'react';

interface CounterProps {
    name: string;
}

export function Counter({ name }: CounterProps) {
    const [count, setCount] = useState<number>(0);

    function onClick(): void {
        setCount(count + 1);
    }

    return (
        <div>
            <h2
                style={{
                    color: 'red',
                    fontSize: 24,
                }}
            >
                {name}'s count: {count}
            </h2>
            <button onClick={onClick}>+</button>
        </div>
    );
}

function App() {
  const { error } = useContext(NoticeContext);

  const [user, setUser] = useState<LoggedInUser>('Loading');
  const loggedIn = () => user instanceof User;
  const userContext = { current: user, loggedIn, update: setUser };

  useEffect(() => {
    sessionApi
      .whoami()
      .then(setUser)
      .catch((e) => error(`Failed to fetch current user: ${e.message}`));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <UserContext.Provider value={userContext}>
      <Router>
        <View.Notices path="/">
          <View.Home path="/" />
          <View.Login path="/login" />

          <View.Issue.Index path="/orgs/:orgId/repos/:repoId/issues" />
          <View.Issue.New path="/orgs/:orgId/repos/:repoId/issues/new" />
          <View.Issue.Show path="/orgs/:orgId/repos/:repoId/issues/:issueId" />

          <View.Org.Index path="/orgs" />
          <View.Org.New path="/orgs/new" />
          <View.Org.Show path="/orgs/:orgId" />

          <View.Org.Repo.Index path="/orgs/:orgId/repos" />
          <View.Org.Repo.New path="/orgs/:orgId/repos/new" />
          <View.Org.Repo.Settings path="/orgs/:orgId/repos/:repoId/settings" />
          <View.Org.Repo.Show path="/orgs/:orgId/repos/:repoId" />

          <View.User.Show path="/users/:userId" />
          <View.User.Repo.Index path="/users/:userId/repos" />

          <View.NotFound default />
        </View.Notices>
      </Router>
    </UserContext.Provider>
  );
}

import { FC } from 'react'
const HelloWorld: FC = () => "Hello, World!"
export default HelloWorld

