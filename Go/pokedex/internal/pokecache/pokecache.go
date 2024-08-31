package pokecache

import (
	"sync"
	"time"
)

type Cache struct {
    mu *sync.Mutex
    data map[string]CacheEntry
}

type CacheEntry struct {
    createdAt time.Time
    val []byte
}

func reapLoop(c *Cache, t time.Duration) {
    ticker := time.NewTicker(10*time.Second)
    go func() {
        for {
            <-ticker.C
            c.mu.Lock()
            var tn time.Time
            for key, val := range c.data {
                tn = time.Now()
                if tn.Sub(val.createdAt) > t {
                    delete(c.data, key)
                }
            }
            c.mu.Unlock()
        }
    }()
}

func NewCache() Cache {
    cache := Cache{&sync.Mutex{}, make(map[string]CacheEntry)}
    reapLoop(&cache, 30*time.Second)
    return cache
}

func (c *Cache) Add(key string, val []byte) {
    defer c.mu.Unlock()
    c.mu.Lock()
    cacheEntry := CacheEntry{time.Now(), val}
    c.data[key] = cacheEntry
}

func (c *Cache) Get(key string) ([]byte, bool){
    defer c.mu.Unlock()
    c.mu.Lock()
    val, ok := c.data[key]
    if !ok {
        return []byte{}, false
    }
    return val.val, true
}
