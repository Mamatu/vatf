#ifndef CALLBACKS_H
#define CALLBACKS_H

#include <functional>
#include <mutex>
#include <vector>

template<typename... Args>
class Callbacks
{
  public:
    Callbacks() = default;
    virtual ~Callbacks() = default;

    int add(std::function<void(Args...)>&& callback)
    {
      std::lock_guard lg(m_mutex);
      m_callbacks.push_back(std::move(callback));
      return m_callbacks.size() - 1;
    }

    void remove(int handler)
    {
      std::lock_guard lg(m_mutex);
      auto it = m_callbacks.begin();
      std::advance(it, handler);
      m_callbacks.erase(it);
    }

  protected:
    void call(Args... args)
    {
      std::lock_guard lg(m_mutex);
      for (const auto& callback: m_callbacks)
      {
        callback(args...);
      }
    }

  private:
    std::mutex m_mutex;
    std::vector<std::function<void(Args...)>> m_callbacks; 
};

template<typename... Args>
class CallbacksCall : public Callbacks<Args...>
{
  public:
    CallbacksCall() = default;
    virtual ~CallbacksCall() = default;

    void call(Args... args)
    {
      Callbacks<Args...>::call(args...);
    }
};

#endif
